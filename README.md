# Simple Music Collaborator

This application is a simple music collaborator powered by the Magenta music transformer. The application can record midi input from the user and use the transformer to generate something new in a similar style. This application was designed to be used in a workshop to give musicians/composers a chance to work with an artificial collaborator so we can better understand what they would want in a co-creative system.

Code to run music transformer orignally from the following Google Music Transformer [notebook](https://colab.research.google.com/notebooks/magenta/piano_transformer/piano_transformer.ipynb).

Porting of notebook to script from the following [repo](https://github.com/Elvenson/piano_transformer).
Our project adds to this work by creating a conditional music transformer class that can be used in an interactive application.

## Installation

You need to install [Magenta](https://github.com/tensorflow/magenta) package (support only Python >= 3.5) with correct version:
```bash
pip install magenta==1.3.1
```

Please look through the requirements.txt file and ensure you utilise libraries with same version. In particular, ensure the version of tensorflow-datasets and pygame are the same to avoid unexpected error messages.

You also need to install `google cloud sdk` to get `Music Transformer` pre-trained model on cloud bucket. To get Google Cloud
SDK please follow this [installation guide](https://cloud.google.com/sdk/docs/downloads-versioned-archives).

You can then download Music Transformer pre-trained model with Google Cloud SDK:
```
gsutil -q -m cp -r gs://magentadata/models/music_transformer/checkpoints/* <destination folder>
```

## Usage
Use the following to run the application:

```bash
python SimpleMusicCollaborator.py
```

If you wish to use the Music Transformer class without the application it is in the *generate_melody.py* file and is initialised using the following:

```bash
music_transformer = MagentaMusicTransformer(model_path)
music_transformer.generate(primer_path)
```

Where *model_path* is the path to music_transformer conditional model and *primer_path* is the path to the midi file that triggers the generation process. 
