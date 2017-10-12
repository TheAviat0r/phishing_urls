import distance
import imagehash

from PIL import Image

def image_distance(first_image_path, second_image_path, hash_size=8):
    try:
        first_image = Image.open(first_image_path)
        second_image = Image.open(second_image_path)

        first_hash = str(imagehash.dhash(first_image, hash_size=hash_size))
        second_hash = str(imagehash.dhash(second_image, hash_size=hash_size))

        return distance.hamming(first_hash, second_hash)
    except IOError as e:
        print('IOError: {0}'.format(e.strerror, ))
        pass

def image_hash(image_name, hash_size=4):
    try:
        with Image.open(image_name) as image:
            image_hash = str(imagehash.dhash(image, hash_size=hash_size))
            return image_hash
    except IOError as e:
        print('IOError: {0} {1}'.format(e.strerror, image_name))
        pass

def hamming_distance(first_hash, second_hash):
    return distance.hamming(first_hash, second_hash)

if __name__ == '__main__':
    print('first hash: ' + image_hash('../first.png'))
    print('second_hash: ' + image_hash('../second.png'))

    sample_test = image_distance('../first.png', '../second.png', hash_size=16)

    print('sample test value: ' + str(sample_test))


