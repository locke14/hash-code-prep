import zipfile
import os
from enum import Enum
import itertools

DATASET_A = "a_example"
DATASET_B = "b_lovely_landscapes"
DATASET_C = "c_memorable_moments"
DATASET_D = "d_pet_pictures"
DATASET_E = "e_shiny_selfies"

INPUT_FORMAT = ".txt"
OUTPUT_FORMAT = ".txt"

DEBUG = True

def log(msg):
    if DEBUG:
        print(msg)


def extension(f):
    return os.path.splitext(f)[1]


def create_code_zip():
    dir_path = './'
    zip_h = zipfile.ZipFile('code.zip', 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if extension(file) == '.py':
                zip_h.write(os.path.join(root, file))

    zip_h.close()


def transition_score(from_slide, to_slide):

    from_tags = from_slide.tag_names
    to_tags = to_slide.tag_names

    s0 = len(from_tags.intersection(to_tags))
    s1 = len(from_tags - to_tags)
    s2 = len(to_tags - from_tags)

    return min(s0, s1, s2)


class Orientation(Enum):
    H = 0
    V = 1


class Photo:
    def __init__(self, photo_id, orientation, tag_names):
        self.photo_id = photo_id
        self.orientation = orientation
        self.tag_names = tag_names

class Slide:
    def __init__(self, slide_id):
        self.slide_id = slide_id
        self.photos = []
        self.orientation = None

    @property
    def num_photos(self):
        return len(self.photos)

    @property
    def tag_names(self):
        tag_names = []
        for photo in self.photos:
            tag_names += photo.tag_names

        return set(tag_names)

    def intersects(self, slide):
        return bool(set(self.photos) & set(slide.photos))

    @property
    def photo_ids(self):
        s = ""
        for photo in self.photos:
            s += str(photo.photo_id) + " "
        return s

    def add_photo(self, photo):
        if self.num_photos == 2:
            log("Already 2 photos in the slide")
            return False

        elif self.num_photos == 1:
            assert self.orientation

            if self.orientation == Orientation.H:
                log("Can't add another photo to a H slide")
                return False

            if photo.orientation == Orientation.H:
                log("Can't add a H photo to a V slide")
                return False

            self.photos.append(photo)
            return True

        elif self.num_photos == 0:
            self.photos.append(photo)
            self.orientation = photo.orientation
            return True

        else:
            assert False


class Tag:
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.photos = []

    def add_photo(self, photo):
        self.photos.append(photo)


class Collection:
    def __init__(self, file_path):
        self.num_photos = 0
        self.photos = []
        self.h_photos = []
        self.v_photos = []
        self.tags = {}
        self._parse_file(file_path)

    def _parse_file(self, file_path):
        with open(file_path, 'r') as f:
            content = f.readlines()
            header = content[0].split()
            self.num_photos = int(header[0])


            photo_id = 0
            for line in content[1:]:
                row = line.split()
                if row[0] == 'H':
                    orientation = Orientation.H
                else:
                    orientation = Orientation.V

                tag_names = row[2:]

                photo = Photo(photo_id, orientation, tag_names)
                self.photos.append(photo)

                if orientation == Orientation.H:
                    self.h_photos.append(photo)
                else:
                    self.v_photos.append(photo)

                for tag_name in tag_names:
                    if tag_name in self.tags:
                        self.tags[tag_name].append(photo)
                    else:
                        self.tags[tag_name] = [photo]

                print(f"Loaded photo with id: {photo_id}")

                photo_id += 1

        print(f"Number of photos in collection: {self.num_photos}")


class PhotoSlideshow:
    def __init__(self, dataset):
        self.collection = Collection(dataset + INPUT_FORMAT)
        self.output_file = dataset + '_output' + OUTPUT_FORMAT
        self.slides = []
        self.all_slides = []

        self.create_all_slides()

    def create_all_slides(self):
        for p in self.collection.h_photos:
            s = Slide(-1)
            s.add_photo(p)
            self.all_slides.append(s)

        for p in list(itertools.combinations(self.collection.v_photos, 2)):
            s = Slide(-1)
            s.add_photo(p[0])
            s.add_photo(p[1])
            self.all_slides.append(s)

        print(len(self.all_slides))

    def write_output(self):
        lines = [str(len(self.slides)) + "\n"]
        for slide in self.slides:
            lines.append(slide.photo_ids + "\n")

        with open(self.output_file, 'w') as f:
            f.writelines(lines)

    def prune_all_slides(self, slide):
        for s in self.all_slides:
            if s.intersects(slide):
                self.all_slides.remove(s)

    def create_slideshow(self):
        curr_slide = self.all_slides[0]

        while self.all_slides:
            print(len(self.all_slides))
            self.slides.append(curr_slide)

            self.prune_all_slides(curr_slide)

            max_score = 0
            for slide in self.all_slides:
                score = transition_score(curr_slide, slide)
                if score > max_score:
                    next_slide = slide

            curr_slide = next_slide

        self.write_output()


    def create_slideshow_fake(self):
        s0 = Slide(0)
        s0.add_photo(self.collection.photos[0])
        self.slides.append(s0)

        s1 = Slide(1)
        s1.add_photo(self.collection.photos[3])
        self.slides.append(s1)

        s2 = Slide(2)
        s2.add_photo(self.collection.photos[1])
        s2.add_photo(self.collection.photos[2])
        self.slides.append(s2)

        print(s0.intersects(s0))

        self.write_output()


def run():
    solver = PhotoSlideshow(DATASET_C)
    solver.create_slideshow()


if __name__ == "__main__":
    run()
