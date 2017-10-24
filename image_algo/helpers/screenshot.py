import os


def get_screenshot(image_dir, website, driver, verbose=False):
    if verbose:
        print('get_screenshot:')
        print(image_dir)

    if not os.path.exists(image_dir):
        if verbose:
            print('DIRECTORY CREATED: ' + image_dir)
        os.mkdir(image_dir)

    driver.get(website.url)

    if os.path.exists(website.screen_path):
        if verbose:
            print('website was already screened: ' + website.screen_path)
        os.remove(website.screen_path)

    driver.save_screenshot(website.screen_path)