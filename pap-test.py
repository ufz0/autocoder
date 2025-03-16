import xml.etree.ElementTree as ET
import subprocess, json, os, shutil

def parse_csharp_code(csharp_code: str):

    formatted_code = csharp_code.replace('"', '""')
    
    script_content = f"""
#r "nuget: Microsoft.CodeAnalysis.CSharp, 4.6.0"

using System;
using System.Text.Json;
using System.Linq;
using System.Collections.Generic;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

string code = @"{formatted_code}";
var tree = CSharpSyntaxTree.ParseText(code);
var root = tree.GetRoot();

var mainMethod = root.DescendantNodes()
    .OfType<MethodDeclarationSyntax>()
    .FirstOrDefault(m => m.Identifier.ValueText == "Main");

int nodeId = 100;
string GetNextId() => (nodeId++).ToString();

object ProcessStatement(StatementSyntax stmt)
{{
    if (stmt is IfStatementSyntax ifStmt)
    {{
        return new {{
            Id = GetNextId(),
            Type = "If",
            Text = ifStmt.Condition.ToString(),
            TrueBranch = ifStmt.Statement is BlockSyntax block 
                ? block.Statements.Select(s => ProcessStatement(s)).ToList() 
                : new List<object> {{ ProcessStatement(ifStmt.Statement) }},
            FalseBranch = ifStmt.Else != null 
                ? (ifStmt.Else.Statement is BlockSyntax elseBlock 
                    ? elseBlock.Statements.Select(s => ProcessStatement(s)).ToList() 
                    : new List<object> {{ ProcessStatement(ifStmt.Else.Statement) }})
                : null
        }};
    }}
    else if (stmt is ForStatementSyntax forStmt)
    {{
        return new {{
            Id = GetNextId(),
            Type = "For",
            Text = (forStmt.Declaration != null ? forStmt.Declaration.ToString() : "") 
                   + " " + (forStmt.Condition != null ? forStmt.Condition.ToString() : ""),
            Body = forStmt.Statement is BlockSyntax block 
                ? block.Statements.Select(s => ProcessStatement(s)).ToList() 
                : new List<object> {{ ProcessStatement(forStmt.Statement) }}
        }};
    }}
    else if (stmt is WhileStatementSyntax whileStmt)
    {{
        return new {{
            Id = GetNextId(),
            Type = "While",
            Text = whileStmt.Condition.ToString(),
            Body = whileStmt.Statement is BlockSyntax block 
                ? block.Statements.Select(s => ProcessStatement(s)).ToList() 
                : new List<object> {{ ProcessStatement(whileStmt.Statement) }}
        }};
    }}
    else if (stmt is ExpressionStatementSyntax exprStmt)
    {{
        var exprText = exprStmt.ToString();
        string nodeType = "Expression";
        if(exprText.Contains("Console.WriteLine")) nodeType = "Output";
        if(exprText.Contains("Console.ReadLine")) nodeType = "Input";
        return new {{
            Id = GetNextId(),
            Type = nodeType,
            Text = exprText
        }};
    }}
    else if (stmt is LocalDeclarationStatementSyntax localDecl)
    {{
        return new {{
            Id = GetNextId(),
            Type = "Declaration",
            Text = localDecl.Declaration.ToString()
        }};
    }}
    else if (stmt is ReturnStatementSyntax returnStmt)
    {{
        return new {{
            Id = GetNextId(),
            Type = "Return",
            Text = returnStmt.ToString()
        }};
    }}
    else if (stmt is BlockSyntax blockStmt)
    {{
        return blockStmt.Statements.Select(s => ProcessStatement(s)).ToList();
    }}
    else
    {{
        return new {{
            Id = GetNextId(),
            Type = stmt.Kind().ToString(),
            Text = stmt.ToString()
        }};
    }}
}}

var flowchart = mainMethod != null 
    ? mainMethod.Body is BlockSyntax mainBlock 
         ? mainBlock.Statements.Select(s => ProcessStatement(s)).ToList() 
         : new List<object>()
    : new List<object>();

Console.WriteLine(JsonSerializer.Serialize(flowchart, new JsonSerializerOptions {{ WriteIndented = true }}));
"""
    
    script_file = "temp_script.csx"
    with open(script_file, "w") as f:
        f.write(script_content)
    # Search the dotnet-script executable.
    dotnet_script = shutil.which("dotnet-script")
    if not dotnet_script:
        print("ERROR: Dotnet_script not installed")
    result = subprocess.run([dotnet_script, script_file], text=True, capture_output=True)
    print("Dotnet script output:")
    print(result.stdout)
    print("Dotnet script error (if any):")
    print(result.stderr)
    os.remove(script_file)
    if result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return None
    else:
        print("Error: No output returned from dotnet script.")
        return None

# --- Layout and Draw.io XML Generation ---

current_y = 20

def layout_nodes(nodes, level=0):
    global current_y
    layout = []
    edges = []
    prev_node_id = None
    for node in nodes:
        if isinstance(node, list):
            sub_layout, sub_edges = layout_nodes(node, level)
            layout.extend(sub_layout)
            edges.extend(sub_edges)
            if sub_layout:
                if prev_node_id:
                    edges.append((prev_node_id, sub_layout[0]['Id'], "next"))
                prev_node_id = sub_layout[-1]['Id']
            continue

        node['x'] = level * 200 + 50
        node['y'] = current_y
        current_y += 100
        layout.append(node)
        if prev_node_id:
            edges.append((prev_node_id, node['Id'], "next"))
        prev_node_id = node['Id']
        for branch in ['TrueBranch', 'FalseBranch', 'Body']:
            if branch in node and node[branch]:
                sub_layout, sub_edges = layout_nodes(node[branch], level+1)
                layout.extend(sub_layout)
                edges.extend(sub_edges)
                if sub_layout:
                    edges.append((node['Id'], sub_layout[0]['Id'], branch))
        for branch in ['TrueBranch', 'FalseBranch', 'Body']:
            if branch in node:
                del node[branch]
    return layout, edges

def generate_drawio_xml(flow_nodes, edges):
    """
    Generates draw.io XML given the list of nodes and edges.
    """
    mxGraphModel = ET.Element("mxGraphModel")
    root = ET.SubElement(mxGraphModel, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    for node in flow_nodes:
        cell = ET.SubElement(root, "mxCell", {
            "id": node["Id"],
            "value": f"{node['Type']}: {node['Text']}",
            "style": "shape=rectangle;rounded=1;",
            "vertex": "1",
            "parent": "1"
        })
        ET.SubElement(cell, "mxGeometry", {"x": str(node["x"]), "y": str(node["y"]), "width": "160", "height": "60", "as": "geometry"})
    edge_id = 1000
    for (src, tgt, label) in edges:
        edge = ET.SubElement(root, "mxCell", {
            "id": str(edge_id),
            "value": label,
            "style": "edgeStyle=elbowEdgeStyle;rounded=0;html=1;",
            "edge": "1",
            "source": src,
            "target": tgt,
            "parent": "1"
        })
        ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
        edge_id += 1
    return ET.tostring(mxGraphModel, encoding="unicode")

if __name__ == "__main__":
    sample_csharp = """
using System;
class Program {{
    static void Main() {{
        int x = 5;
        Console.WriteLine("Start");
        if (x > 3) {{
            Console.WriteLine("x is greater than 3");
        }} else {{
            Console.WriteLine("x is not greater than 3");
        }}
        for (int i = 0; i < 3; i++) {{
            Console.WriteLine(i);
        }}
        while (x > 0) {{
            Console.WriteLine(x);
            x--;
        }}
        Console.ReadLine();
    }}
}}
"""
    flowchart_json = parse_csharp_code(sample_csharp)
    if flowchart_json:
        nodes, edges = layout_nodes(flowchart_json, level=0)
        xml_output = generate_drawio_xml(nodes, edges)
        with open("output.drawio", "w") as f:
            f.write(xml_output)
        print("Draw.io XML erzeugt: output.drawio")
