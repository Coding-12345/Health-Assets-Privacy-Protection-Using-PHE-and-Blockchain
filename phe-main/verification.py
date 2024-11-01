import model

data = [40,0,1,140,289,0,0,172,0,0]
model_coefficients = model.model_output()
print("Prediction value:", sum([data[i] * model_coefficients[i] for i in range(len(data))]))