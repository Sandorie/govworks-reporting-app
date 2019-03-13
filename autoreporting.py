from jinja2 import FileSystemLoader, Environment

'''
# Content to be published
content = "Govworks_Reporting_Tool"
'''
# Configure Jinja and ready the template
env = Environment(
    loader=FileSystemLoader(searchpath="templates")
)

#Use this to assemble the templaters
base_template = env.get_template("report.html")
table_section_template = env.get_template("table_section.html")

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

def main():
    """
    Entry point for the script.
    Render a template and write it to file.
    :return:
   """ 
    with open("outputs/report.html", "w") as f:
        f.write(base_template.render(
            title=title,
            sections=sections
        ))

if __name__ == "__main__":
    main()


  

