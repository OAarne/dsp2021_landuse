Before using these scripts, you'll need to set up a Python virtual environment and install the dependencies listed in `requirements.txt`. If you don't know how to do that, I'm sure Google will be helpful.

Once you've got the virtual environment set up, you can use `evaluation.ipynb`, `confusion_matrix.ipynb`, and `visualize.ipynb` to analyze the results of your classifier. `evaluation.ipynb` contains more detailed instructions for this.

Additionally, the repo includes `xlsx_to_csv.py` and `validation_test_split.py`, that are used to generate the CSV files used by the aforementioned scripts from the original .xlsx files.

## Configuration

- Make a new copy of `example_config.yaml` and rename it to `config.yaml`
- Use the config file to specify which result files you want to include in the evaluation

## Running the visualizer locally

- Run `voila visualize.ipynb`
- Loading the app takes a while. Note that the app is fully loaded once you are able to see maps being displayed.

## Deploying the visualizer to Heroku

- The visualizer is accesible at https://hexa-visualizer.herokuapp.com/
- For deploying a new version with more data refer to Heroku documentation. See for example: https://devcenter.heroku.com/articles/getting-started-with-python


