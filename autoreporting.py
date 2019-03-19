import os

import pandas as pd
from jinja2 import Environment, FileSystemLoader

#The following comand line allows for wide columns - if not, columns will be spaced and ellipsed 
pd.set_option("display.max_colwidth", 200)

class ModelResults:
    def __init__(self, model_name, filepath):
        """
        :param model_name: Name of model.
        :param filepath: Filepath to results .csv.
        """
        print("----> init")
        self.model_name = model_name
        print("----> " + self.model_name)
        self.filepath = filepath
        print("----> " + self.filepath)
        self.dataset = os.path.split(filepath)[-1]
        print("----> " + self.dataset)
        self.df_results = csv_to_df(filepath)  # Filesystem access
        print("----> ", self.df_results)
        self.number_of_images = len(self.df_results)
        print("----> ", self.number_of_images)
        self.accuracy = self._calculate_accuracy()
        print("----> ", self.accuracy)

        self.misidentified_images = self._get_misidentified_images()
        print("---->", self.misidentified_images)
        self.number_misidentified = len(self.misidentified_images)
        print("---->", self.number_misidentified)

    def _calculate_accuracy(self):
        """
        Return the accuracy for the dataset.
        :return: Float of dataset accuracy [0..1].
        """
        print("calculate_accuracy")
        number_correct = len(self.df_results[self.df_results["correct"] == True])
        number_total = len(self.df_results)
        print("Number TOTAL", number_total)
        return number_correct / number_total

    def _get_misidentified_images(self):
        """
        Return the names misidentified images.
        :return: List of strings of misidentified image filenames.
        """
        print("get misidentified images")
        df_misidentified = self.df_results[self.df_results["correct"] == False]
        misidentified_images = df_misidentified.index.tolist()
        return misidentified_images

    def get_results_df_as_html(self):
        """
        Return the results DataFrame as an HTML object.
        :return: String of HTML.
        """
        print("get results df as html")
        html = self.df_results.to_html()
        return html


def csv_to_df(filepath):
    """
    Open a .csv file and return it in DataFrame format.
    :param filepath: Filepath to a .csv file to be read.
    :return: .csv file in DataFrame format.
    """
    print("csv to df")
    df = pd.read_csv(filepath, index_col=0)
    return df


def common_misidentified_images(list_model_results):
    """
    For a collection of ModelResults objects, return a list of images names that were misidentified by all.
    :param list_model_results: List of ModelResults objects.
    :return: List of common misidentified image names.
    """
    print("common_misidentified_images")

    misidentified_images_sets = [set(model_results.misidentified_images) for model_results in list_model_results]
    common_images = set.intersection(*misidentified_images_sets)
    return common_images

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
    """
    print("main")
    vgg19_model = ModelResults("VGG19", "./datasets/VGG19_results.csv")
    vgg19_results = vgg19_model.get_results_df_as_html()

    mobilenet_model = ModelResults("MobileNet", "./datasets/MobileNet_results.csv")
    mobilenet_results = mobilenet_model.get_results_df_as_html()
"""
    #Content to be published 
    title = "Model Report"
    vgg19_results = ModelResults("VGG19", "datasets/VGG19_results.csv")
    mobilenet_results = ModelResults("MobileNet", "datasets/MobileNet_results.csv")
    number_misidentified = len(set(vgg19_results.misidentified_images) & set(mobilenet_results.misidentified_images))


    # This is used to produce section block.
    sections = list()
    sections.append(table_section_template.render(
    model="VGG19",
    dataset="VGG19_results.csv",
    table="Table goes here."
    ))
    sections.append(vgg19_results)
    sections.append(table_section_template.render(
    model="MobileNet",
    dataset="MobileNet_results.csv",
    table="Table goes here."
    ))
    sections.append(mobilenet_results)
    
    with open("outputs/report.html", "w") as f:
        f.write(base_template.render(
            title=title,
            sections=sections
        ))

if __name__ == "__main__":
    main()