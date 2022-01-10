
import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.datasets.folder import default_loader





print('Load model: vgg19')
model = torchvision.models.vgg19(True)
# print(model)

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
trans = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    normalize,
])


def get_image_hash(path: str) -> np.ndarray:
    input_image = default_loader(path)
    input_image = trans(input_image)
    input_image = torch.unsqueeze(input_image, 0)
    image_feature = model.features(input_image)
    # print(image_feature)
    image_feature = image_feature.detach().numpy()
    image_feature = np.reshape(image_feature[0], -1)
    image_feature = image_feature / np.linalg.norm(image_feature)
    return image_feature




if __name__ == '__main__':
    r = get_image_hash('in.png')
    print(np.sum(r), r.shape)
