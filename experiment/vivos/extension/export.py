import shutil
from os.path import join


class SphinxSpeechRecognitionExporter:
    @staticmethod
    def export(model, export_folder):
        tmp_folder = model.tmp_folder
        try:
            shutil.rmtree(join(export_folder, "etc"))
        except:
            pass
        finally:
            shutil.copytree(join(tmp_folder, "etc"),
                            join(export_folder, "etc"))

        try:
            shutil.rmtree(join(export_folder, "model_parameters"))
        except:
            pass
        finally:
            shutil.copytree(join(tmp_folder, "model_parameters"),
                            join(export_folder, "model_parameters"))
