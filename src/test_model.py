import cv2
import torch
from src.model.DCGAN import Generator, Discriminator
import matplotlib.pyplot as plt

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
G = Generator(100).to(DEVICE)
D = Discriminator(3).to(DEVICE)


G.load_state_dict(torch.load("./checkpoints/G.pth"))
D.load_state_dict(torch.load("./checkpoints/D.pth"))

G.eval()
noise = torch.randn(10, 100).to(DEVICE)
fake_imgs = G(noise)
# img = cv2.resize(fake_imgs[0].permute(1, 2, 0).detach().cpu().numpy(), (512, 512))
# print(img.shape)
# plt.imshow(img)
# make grids
fig = plt.figure(figsize=(10, 10))
for i in range(10):
    img = cv2.resize(fake_imgs[i].permute(1, 2, 0).detach().cpu().numpy(), (512, 512))
    img = (img + 1) / 2
    fig.add_subplot(2, 5, i + 1)
    plt.imshow(img)

plt.show()
