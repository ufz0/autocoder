from datetime import date

def get_bhc(name, summary):
    formatted_date = date.today().strftime("%d/%m/%Y")
    comment = f"""
/*--------------------------------------------------------------
 *              HTBLA-Leonding / Class: 1BHIF
 *--------------------------------------------------------------
 *              {name}, {formatted_date}
 *--------------------------------------------------------------
 * Description:
 * {summary}
 *--------------------------------------------------------------
*/


"""
    return comment