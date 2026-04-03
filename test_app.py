import pandas as pd
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.pipeline.training_pipeline import TrainingPipeline

def test_predict():
    try:
        print("Testing predict...")
        df=pd.read_csv("Network_Data/phisingData.csv")
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        y_pred = network_model.predict(df)
        print("Predict SUCCESS, first 5 outputs:", y_pred[:5])
    except Exception as e:
        import traceback
        traceback.print_exc()

def test_train():
    try:
        print("Testing train...")
        tp = TrainingPipeline()
        tp.run_pipeline()
        print("Train SUCCESS")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_predict()
    test_train()
