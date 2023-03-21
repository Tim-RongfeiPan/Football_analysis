import argparse
import os
from util import util
import torch
import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

WEIGHTS = ROOT / 'weights'


class BaseOptions():

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.initialized = False

    def initialize(self, directory):
        #required=True
        self.parser.add_argument('--image',
                                 required=False,
                                 type=str,
                                 help='sth like "./my_pic.png" ')
        self.parser.add_argument('--advertising_image',
                                 required=False,
                                 type=str,
                                 help='sth like "./my_billboard.png" ')

        self.parser.add_argument(
            '--dataroot',
            type=str,
            default=directory +
            r'\pytorch-two-GAN-master\datasets\soccer_seg_detection',
            help=
            'path to images (should have subfolders trainA, trainB, valA, valB, etc)'
        )
        self.parser.add_argument('--batchSize',
                                 type=int,
                                 default=1,
                                 help='input batch size')
        self.parser.add_argument('--loadSize',
                                 type=int,
                                 default=1024,
                                 help='scale images to this size')
        self.parser.add_argument('--fineSize',
                                 type=int,
                                 default=1024,
                                 help='then crop to this size')
        self.parser.add_argument('--input_nc',
                                 type=int,
                                 default=3,
                                 help='# of input image channels')
        self.parser.add_argument('--output_nc',
                                 type=int,
                                 default=1,
                                 help='# of output image channels')
        self.parser.add_argument('--ngf',
                                 type=int,
                                 default=64,
                                 help='# of gen filters in first conv layer')
        self.parser.add_argument(
            '--ndf',
            type=int,
            default=64,
            help='# of discrim filters in first conv layer')
        self.parser.add_argument('--which_model_netD',
                                 type=str,
                                 default='basic',
                                 help='selects model to use for netD')
        self.parser.add_argument('--which_model_netG',
                                 type=str,
                                 default='unet_256',
                                 help='selects model to use for netG')
        self.parser.add_argument(
            '--n_layers_D',
            type=int,
            default=3,
            help='only used if which_model_netD==n_layers')
        self.parser.add_argument(
            '--gpu_ids',
            type=str,
            default='-1',
            help='gpu ids: e.g. 0  0,1,2, 0,2. use -1 for CPU')
        self.parser.add_argument(
            '--name',
            type=str,
            default=directory +
            r'\pytorch-two-GAN-master\checkpoints\soccer_seg_detection_pix2pix',
            help=
            'name of the experiment. It decides where to store samples and models'
        )
        self.parser.add_argument(
            '--dataset_mode',
            type=str,
            default='single',
            help=
            'chooses how datasets are loaded. [unaligned | aligned | single]')
        self.parser.add_argument(
            '--model',
            type=str,
            default='two_pix2pix',
            help='chooses which model to use. cycle_gan, pix2pix, test, ')
        self.parser.add_argument('--which_direction',
                                 type=str,
                                 default='AtoB',
                                 help='AtoB or BtoA')
        self.parser.add_argument('--nThreads',
                                 default=2,
                                 type=int,
                                 help='# threads for loading data')
        self.parser.add_argument('--checkpoints_dir',
                                 type=str,
                                 default=directory +
                                 '\pytorch-two-GAN-master\checkpoints',
                                 help='models are saved here')
        self.parser.add_argument(
            '--norm',
            type=str,
            default='batch',
            help='instance normalization or batch normalization')
        self.parser.add_argument(
            '--serial_batches',
            action='store_true',
            help=
            'if true, takes images in order to make batches, otherwise takes them randomly'
        )
        self.parser.add_argument('--display_winsize',
                                 type=int,
                                 default=256,
                                 help='display window size')
        self.parser.add_argument('--display_id',
                                 type=int,
                                 default=1,
                                 help='window id of the web display')
        self.parser.add_argument('--display_port',
                                 type=int,
                                 default=8097,
                                 help='visdom port of the web display')
        self.parser.add_argument('--no_dropout',
                                 action='store_true',
                                 help='no dropout for the generator')
        self.parser.add_argument(
            '--max_dataset_size',
            type=int,
            default=float("inf"),
            help=
            'Maximum number of samples allowed per dataset. If the dataset directory contains more than max_dataset_size, only a subset is loaded.'
        )
        self.parser.add_argument(
            '--resize_or_crop',
            type=str,
            default='resize_and_crop',
            help=
            'scaling and cropping of images at load time [resize_and_crop|crop|scale_width|scale_width_and_crop]'
        )
        self.parser.add_argument(
            '--no_flip',
            action='store_true',
            help='if specified, do not flip the images for data augmentation')
        self.parser.add_argument(
            '--init_type',
            type=str,
            default='normal',
            help='network initialization [normal|xavier|kaiming|orthogonal]')

        self.parser.add_argument('--weights',
                                 nargs='+',
                                 type=str,
                                 default=ROOT / 'yolov5s.pt',
                                 help='model path or triton URL')
        self.parser.add_argument('--source',
                                 type=str,
                                 default=ROOT / 'data/images',
                                 help='file/dir/URL/glob/screen/0(webcam)')

        # tracking parser options
        self.parser.add_argument('--yolo-weights',
                                 nargs='+',
                                 type=Path,
                                 default=WEIGHTS / 'yolov5m.pt',
                                 help='model.pt path(s)')
        self.parser.add_argument('--strong-sort-weights',
                                 type=Path,
                                 default=WEIGHTS / 'osnet_x0_25_msmt17.pt')
        self.parser.add_argument(
            '--config-strongsort',
            type=str,
            default='strong_sort/configs/strong_sort.yaml')
        # self.parser.add_argument('--source', type=str, default='0',
        #                     help='file/dir/URL/glob, 0 for webcam')
        self.parser.add_argument('--imgsz',
                                 '--img',
                                 '--img-size',
                                 nargs='+',
                                 type=int,
                                 default=[640],
                                 help='inference size h,w')
        self.parser.add_argument('--conf-thres',
                                 type=float,
                                 default=0.5,
                                 help='confidence threshold')
        self.parser.add_argument('--iou-thres',
                                 type=float,
                                 default=0.5,
                                 help='NMS IoU threshold')
        self.parser.add_argument('--max-det',
                                 type=int,
                                 default=1000,
                                 help='maximum detections per image')
        self.parser.add_argument('--device',
                                 default='',
                                 help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
        self.parser.add_argument('--show-vid',
                                 action='store_true',
                                 help='display tracking video results')
        self.parser.add_argument('--show-team',
                                 type=Path,
                                 default=WEIGHTS / 'frej-bp.txt',
                                 help='save and show team assignment')
        self.parser.add_argument('--save-txt',
                                 action='store_true',
                                 help='save results to *.txt')
        self.parser.add_argument('--save-conf',
                                 action='store_true',
                                 help='save confidences in --save-txt labels')
        self.parser.add_argument('--save-crop',
                                 action='store_true',
                                 help='save cropped prediction boxes')
        self.parser.add_argument('--save-vid',
                                 action='store_true',
                                 help='save video tracking results')
        self.parser.add_argument('--show-perstrans',
                                 action='store_true',
                                 help='show perspective transformation result')
        self.parser.add_argument('--nosave',
                                 action='store_true',
                                 help='do not save images/videos')
        # class 0 is person, 1 is bycicle, 2 is car... 79 is oven
        self.parser.add_argument(
            '--classes',
            nargs='+',
            type=int,
            help='filter by class: --classes 0, or --classes 0 2 3')
        self.parser.add_argument('--agnostic-nms',
                                 action='store_true',
                                 help='class-agnostic NMS')
        self.parser.add_argument('--augment',
                                 action='store_true',
                                 help='augmented inference')
        self.parser.add_argument('--visualize',
                                 action='store_true',
                                 help='visualize features')
        self.parser.add_argument('--update',
                                 action='store_true',
                                 help='update all models')
        self.parser.add_argument('--project',
                                 default=ROOT / 'runs/track',
                                 help='save results to project/name')
        # self.parser.add_argument('--name', default='exp',
        #                     help='save results to project/name')
        self.parser.add_argument(
            '--exist-ok',
            action='store_true',
            help='existing project/name ok, do not increment')
        self.parser.add_argument('--line-thickness',
                                 default=3,
                                 type=int,
                                 help='bounding box thickness (pixels)')
        self.parser.add_argument('--hide-labels',
                                 default=False,
                                 action='store_true',
                                 help='hide labels')
        self.parser.add_argument('--hide-conf',
                                 default=False,
                                 action='store_true',
                                 help='hide confidences')
        self.parser.add_argument('--hide-class',
                                 default=False,
                                 action='store_true',
                                 help='hide IDs')
        self.parser.add_argument('--half',
                                 action='store_true',
                                 help='use FP16 half-precision inference')

        self.parser.add_argument('--no-strongSort',
                                 default=False,
                                 action='store_true',
                                 help='disable strong sort')
        self.parser.add_argument('--dnn',
                                 action='store_true',
                                 help='use OpenCV DNN for ONNX inference')
        self.parser.add_argument('--eval',
                                 action='store_true',
                                 help='run evaluation')
        self.initialized = True

    def parse(self, directory):
        if not self.initialized:
            self.initialize(directory)
        self.opt = self.parser.parse_args()
        self.opt.isTrain = self.isTrain  # train or test

        str_ids = self.opt.gpu_ids.split(',')
        self.opt.gpu_ids = []
        for str_id in str_ids:
            id = int(str_id)
            if id >= 0:
                self.opt.gpu_ids.append(id)

        # set gpu ids
        if len(self.opt.gpu_ids) > 0:
            torch.cuda.set_device(self.opt.gpu_ids[0])

        args = vars(self.opt)

        #print('------------ Options -------------')
        #for k, v in sorted(args.items()):
        #    print('%s: %s' % (str(k), str(v)))
        #print('-------------- End ----------------')

        # save to the disk
        expr_dir = os.path.join(self.opt.checkpoints_dir, self.opt.name)
        util.mkdirs(expr_dir)
        file_name = os.path.join(expr_dir, 'opt.txt')
        with open(file_name, 'wt') as opt_file:
            opt_file.write('------------ Options -------------\n')
            for k, v in sorted(args.items()):
                opt_file.write('%s: %s\n' % (str(k), str(v)))
            opt_file.write('-------------- End ----------------\n')
        return self.opt
