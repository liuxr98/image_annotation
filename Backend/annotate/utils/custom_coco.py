from sahi.utils.coco import CocoAnnotation, Coco


class CustomCocoAnnotation(CocoAnnotation):
    def __init__(
            self,
            segmentation=None,
            bbox=None,
            category_id=None,
            category_name=None,
            image_id=None,
            iscrowd=0,
            attributes=[]  # add custom attributes support
    ):
        super().__init__(
            segmentation=segmentation,
            bbox=bbox,
            category_id=category_id,
            category_name=category_name,
            image_id=image_id,
            iscrowd=iscrowd,
        )
        self._attributes = attributes

    @property
    def attributes(self):
        """
            Return custom attributes of the annotation
        """
        if self._attributes:
            return self._attributes
        return {}


class CustomCoco(Coco):
    @property
    def json(self):
        return create_coco_dict(
            images=self.images,
            categories=self.json_categories,
            ignore_negative_samples=self.ignore_negative_samples,
        )


def create_coco_dict(images, categories, ignore_negative_samples=False):
    """
    Creates COCO dict with fields "images", "annotations", "categories".
    Arguments
    ---------
        images : List of CocoImage containing a list of CocoAnnotation
        categories : List of Dict
            COCO categories
        ignore_negative_samples : Bool
            If True, images without annotations are ignored
    Returns
    -------
        coco_dict : Dict
            COCO dict with fields "images", "annotations", "categories"
    """
    out_images = []
    out_annotations = []
    out_categories = categories

    num_images = len(images)
    image_id = 1
    annotation_id = 1
    for image_ind in range(num_images):
        # get coco image and its coco annotations
        coco_image = images[image_ind]
        coco_annotations = coco_image.annotations
        # get num annotations
        num_annotations = len(coco_annotations)
        # if ignore_negative_samples is True and no annotations, skip image
        if ignore_negative_samples and num_annotations == 0:
            continue
        else:
            # create coco image object
            out_image = {
                "height": coco_image.height,
                "width": coco_image.width,
                "id": image_id,
                "file_name": coco_image.file_name,
            }
            out_images.append(out_image)

            # do the same for image annotations
            for coco_annotation in coco_annotations:
                # create coco annotation object
                out_annotation = {
                    "iscrowd": 0,
                    "image_id": image_id,
                    "bbox": coco_annotation.bbox,
                    "segmentation": coco_annotation.segmentation,
                    "category_id": coco_annotation.category_id,
                    "id": annotation_id,
                    "area": coco_annotation.area,
                    "attributes": coco_annotation.attributes
                }

                out_annotations.append(out_annotation)
                annotation_id = annotation_id + 1

            # increment annotation id
            image_id = image_id + 1

    # form coco dict
    coco_dict = {
        "images": out_images,
        "annotations": out_annotations,
        "categories": out_categories,
    }
    # return coco dict
    return coco_dict
