from container import ElementBase
from image_algo.config import TARGET_IMAGE_DIR
from image_algo.helpers.screenshot import get_screenshot
from neuro_algo.config import TARGET_NEURO_DIR
from neuro_algo.preprocessing_crop_minify import crop_minify
import caffe


class NeuroAlgoTarget(ElementBase):
    def __init__(self, url, target_name, driver, net, pca, *args, **kwargs):
        super(NeuroAlgoTarget, self).__init__(url, *args, **kwargs)
        self.name = target_name
        self.screen_path = TARGET_NEURO_DIR + '/' + self.name + '.png'

        get_screenshot(TARGET_NEURO_DIR, self, driver)
        crop_minify(self.screen_path)
        self.screen_path = self.screen_path.replace('.png', '.jpg')
        img = caffe.io.load_image(self.screen_path)
        img = img[:, :, ::-1] * 255.0  # convert RGB->BGR
        img = img.transpose((2, 0, 1))
        img = img[None, :]  # add singleton dimension
        out = net.forward_all(data=img)
        self.coords = pca.transform(out['features'].flatten().reshape(1,-1))

    def __str__(self):
        output = '------------------------\n'
        output += 'target_name: ' + self.name + '\n'
        output += 'url: ' + self.url + '\n'
        output += 'screen_path: ' + self.screen_path + '\n'
        output += 'coords: ' + self.coords + '\n'
        output += '------------------------'

        return output