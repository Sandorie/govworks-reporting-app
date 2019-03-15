import pandas as pd sys.path.insert(0,/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages)
from jinja2 import FileSystemLoader, Environment


#The following comand line allows for wide columns - if not, columns will be spaced and ellipsed 
pd.set_option("display.max_colwidth", 200)

def csv_to_html(filepath):
    """
    This will open a .csv file and return it in a HTML format.
    :param filepath: this is the Filepath to a .csv file to be read. 
    :return: String of HTML to be published.
    """
    df = pd.read_csv(filepath, index_col=0)
    html = df.to_html()
    return html 

'''
# Content to be published
content = "Govworks_Reporting_Tool"
'''
# Configure Jinja and ready the template
env = Environment(
    loader=FileSystemLoader(searchpath="templates")
)

#Use this to assemble the templates
base_template = env.get_template("report.html")
table_section_template = env.get_template("table_section.html")



def main():
    """
    Entry point for the script.
    Render a template and write it to file.
    :return:
   """ 

    #Content to be published 
    title = "Model Report"
    sections = list()
    sections.append(table_section_template.render(
    model="VGG19",
    dataset="VGG19_results.csv",
    table="Table goes here."
    ))
    sections.append(table_section_template.render(
    model="MobileNet",
    dataset="MobileNet_results.csv",
    table="Table goes here."
    ))
    
    with open("outputs/report.html", "w") as f:
        f.write(base_template.render(
            title=title,
            sections=sections
        ))

if __name__ == "__main__":
    main()


  

