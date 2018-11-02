# Q2-9
# =======================Stochastic Gradient Descent.
# torch.optim.SGD
# Batch Size : 1
# ====== Training Time 234.262710
# Accuracy of the network on the 10000 test images: 85 %
# Predicted:  Sandal
# Accuracy of Tshirt : 88 %
# Accuracy of Trouser : 95 %
# Accuracy of Pullover : 84 %
# Accuracy of Dress : 82 %
# Accuracy of  Coat : 76 %
# Accuracy of Sandal : 93 %
# Accuracy of Shirt : 51 %
# Accuracy of Sneaker : 95 %
# Accuracy of   Bag : 95 %
# Accuracy of Ankleboot : 91 %

# =======================Batch Gradient Descent
# torch.optim.ASGD
# Batch Size : 1
# ====== Training Time 267.819059
# Accuracy of the network on the 10000 test images: 85 %
# Predicted:  Sandal
# Accuracy of Tshirt : 82 %
# Accuracy of Trouser : 95 %
# Accuracy of Pullover : 79 %
# Accuracy of Dress : 85 %
# Accuracy of  Coat : 74 %
# Accuracy of Sandal : 94 %
# Accuracy of Shirt : 63 %
# Accuracy of Sneaker : 89 %
# Accuracy of   Bag : 95 %
# Accuracy of Ankleboot : 95 %

# =======================Mini Batch Gradient Descent
# torch.optim.ASGD
# Batch Size : 64
# ====== Training Time 28.686411
# Accuracy of the network on the 10000 test images: 66 %
# Predicted:  Dress
# Accuracy of Tshirt : 55 %
# Accuracy of Trouser : 77 %
# Accuracy of Pullover : 70 %
# Accuracy of Dress : 87 %
# Accuracy of  Coat : 52 %
# Accuracy of Sandal :  0 %
# Accuracy of Shirt : 13 %
# Accuracy of Sneaker : 88 %
# Accuracy of   Bag : 87 %
# Accuracy of Ankleboot : 78 %


# --------------------------------------------------------------------------------------------
import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import torch.nn as nn
from torch.autograd import Variable
import time

# --------------------------------------------------------------------------------------------
input_size = 28*28
hidden_size = 100
num_classes = 10
num_epochs = 5
batch_size = 64
learning_rate = 0.001
# --------------------------------------------------------------------------------------------
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
# --------------------------------------------------------------------------------------------
train_set = torchvision.datasets.FashionMNIST(root='./data_fashion', train=True, download=True, transform=transforms.ToTensor())

train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)

testset = torchvision.datasets.FashionMNIST(root='./data_fashion', train=False, download=True, transform=transforms.ToTensor())

test_loader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False)

# # Find the right classes name. Save it as a tuple of size 10.
classes =("Tshirt", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankleboot")

def imshow(img):
    img = img / 2 + 0.5
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))

dataiter = iter(train_loader)
images, labels = dataiter.next()

imshow(torchvision.utils.make_grid(images))
plt.show()

print(' '.join('%5s' % classes[labels[j]] for j in range(1)))

# --------------------------------------------------------------------------------------------
class Net(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()         # nn.LeakyReLU()        # nn.ELU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# --------------------------------------------------------------------------------------------
net = Net(input_size, hidden_size, num_classes)
net.cuda()

# --------------------------------------------------------------------------------------------
criterion = nn.CrossEntropyLoss()
#optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)
##### -----  Q3 Implements Averaged Stochastic Gradient Descent.
optimizer = torch.optim.ASGD(net.parameters(), lr=learning_rate)        # Batch or Mini-Batch
#optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate)        # stochastic gradient descent

# --------------------------------------------------------------------------------------------
start = time.time()
for epoch in range(num_epochs):
    for i, data in enumerate(train_loader):
        images, labels = data
        images= images.view(-1, 28 * 28).cuda()
        images, labels = Variable(images), Variable(labels.cuda())
        optimizer.zero_grad()
        outputs = net(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        if (i + 1) % 100 == 0:
            print('Epoch [%d/%d], Step [%d/%d], Loss: %.4f'
                  % (epoch + 1, num_epochs, i + 1, len(train_set) // batch_size, loss.data[0]))


end = time.time()
print('====== Training Time %f' % (end-start))

# --------------------------------------------------------------------------------------------
# There is bug here find it and fix it
correct = 0
total = 0
for images, labels in test_loader:
    images = Variable(images.view(-1, 28*28)).cuda()
    outputs = net(images)
    _, predicted = torch.max(outputs.data, 1)
    total += labels.size(0)
    correct += (predicted.cpu() == labels).sum()

print('Accuracy of the network on the 10000 test images: %d %%' % (100 * correct / total))
# --------------------------------------------------------------------------------------------

_, predicted = torch.max(outputs.data, 1)
print('Predicted: ', ' '.join('%5s' % classes[predicted[j]] for j in range(1)))
# --------------------------------------------------------------------------------------------
class_correct = list(0. for i in range(10))
class_total = list(0. for i in range(10))
for data in test_loader:
    images, labels = data
    images = Variable(images.view(-1, 28*28)).cuda()
    outputs = net(images)
    _, predicted = torch.max(outputs.data, 1)
    labels = labels.cpu().numpy()
    c = (predicted.cpu().numpy() == labels)
    for i in range(1):
        label = labels[i]
        class_correct[label] += c[i]
        class_total[label] += 1

# --------------------------------------------------------------------------------------------
for i in range(10):
    print('Accuracy of %5s : %2d %%' % (classes[i], 100 * class_correct[i] / class_total[i]))
# --------------------------------------------------------------------------------------------

torch.save(net.state_dict(), 'model.pkl')