import torch
from torch import nn
from tqdm.auto import tqdm
import os

def train_multiclass(model, dataset ,device, epochs,test_dataset=None ,Optimizer='SGD', learning_rate=0.01):
  import os
  from tqdm.auto import tqdm
  import torch
  from torch import nn

  try:
    from torchmetrics import Accuracy
  except Exception as e:
    if str(e)=="No module named 'torchmetrics'":
      os.system("pip install torchmetrics")
      from torchmetrics import Accuracy
    else:
      print(e)

  epoch_list=[]
  train_loss_list=[]
  train_accuracy_list=[]
  test_loss_list=[]
  test_accuracy_list=[]

  model=model.to(device)
  loss_fn=nn.CrossEntropyLoss()
  activation=nn.Softmax(dim=1)
  accuracy_fn=Accuracy().to(device)

  if Optimizer=='adam':
    optimizer=torch.optim.Adam(params=model.parameters(), lr=learning_rate)
  else:
    optimizer=torch.optim.SGD(params=model.parameters(), lr=learning_rate)
  
  model.train()
  
  train_loss=0
  train_accuracy=0

  for epoch in tqdm(range(epochs)):
    for batch, (x, y) in enumerate(dataset):
      x_train=x.to(device)
      y_train=y.to(device)

      model.train()
      y_logits = model(x_train)
      y_preds=activation(y_logits).argmax(dim=1)
      loss=loss_fn(y_logits, y_train)
      accuracy=accuracy_fn(y_preds, y_train)

      train_loss += loss
      train_accuracy += accuracy

      optimizer.zero_grad()
      loss.backward()
      optimizer.step()
    train_loss /= len(dataset)
    train_accuracy /= len(dataset)

    with torch.inference_mode():
      train_loss_list.append(float(train_loss))
      train_accuracy_list.append(float(train_accuracy))
      epoch_list.append(epoch)

    if test_dataset !=None:
      model.eval()
      test_loss=0
      test_accuracy=0

      with torch.inference_mode():
        for x2 ,y2 in test_dataset:
          x_test=x2.to(device)
          y_test=y2.to(device)

          test_logits=model(x_test)
          test_preds=activation(test_logits).argmax(dim=1)
          loss2=loss_fn(test_logits, y_test)
          accuracy2=accuracy_fn(test_preds, y_test)
          test_loss+=loss2
          test_accuracy+=accuracy2
        test_loss /= len(test_dataset)
        test_accuracy /= len(test_dataset)

        test_loss_list.append(float(test_loss))
        test_accuracy_list.append(float(test_accuracy))

      print(f'Epoch: {epoch+1} || Train Loss: {train_loss:.4f} || Train Accuracy: {train_accuracy*100:.4f} % || Test Loss: {test_loss:.4f} | Test Accuacy: {test_accuracy*100:.4f}')
    else:
      print(f'Epoch: {epoch+1} || Loss: {train_loss:.4f} || Accuracy: {train_accuracy*100:.4f} %')
  if test_dataset !=None:
    return {"Epoch":epoch_list, "Train Loss": train_loss_list, "Train Accuracy": train_accuracy_list, "Test Loss":test_loss_list, "Test Accuracy": test_accuracy_list}
  else:
    return {"Epoch":epoch_list, "Train Loss": train_loss_list, "Train Accuracy": train_accuracy_list}

      
