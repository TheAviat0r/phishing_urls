from image_algo.image_algo import ImageAlgo
from image_algo.supply import ImageAlgoTarget
from urls_algo.urls_algo import UrlsAlgo
from .global_config import *
from selenium import webdriver

# хотелось бы, чтобы запуск алгоритмов происходил исходя из конфига, то-есть,
# чтобы не приходилось сюда дописывать ImageAlgoTarget(...), или AnotherAlgoTarget(...)
# чтобы информация читалась из конфига и таргетам алгоритмов передавались нужные параметры

if __name__ == '__main__':
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 768)

    targets = []
    for key, value in source_websites.items():
        targets.append(ImageAlgoTarget(value, key, driver))

    algo1 = UrlsAlgo('urls.txt')
    algo1.run()
    algo1.answers()

    algo2 = ImageAlgo('urls.txt', targets)
    algo2.run(driver)
    algo2.answers()

    driver.quit()
