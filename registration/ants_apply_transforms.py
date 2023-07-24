import argparse
import ants
"""reference
https://antspy.readthedocs.io/en/latest/registration.html

python ants_apply_transforms.py --moving-image moving_image.nii.gz --fixed-image fixed_image.nii.gz --output-image output_image.nii.gz --input-transform transform.mat transform1.mat 
"""

# 创建一个命令行解析器
parser = argparse.ArgumentParser(description='ANTS registration script')

# 添加需要的命令行参数
parser.add_argument('--moving-image', type=str, help='path to moving image')
parser.add_argument('--fixed-image', type=str, help='path to fixed image')
parser.add_argument('--output-image', type=str, help='path to output image')
parser.add_argument('--imagetype', type=int, default=0, help='choose 0/1/2/3 mapping to scalar/vector/tensor/time-series')
parser.add_argument('--input-transform', type=str, nargs='+', default=['transform.mat'],
                    help='path to input transform files')

# 解析命令行参数
args = parser.parse_args()

# 读取固定图像和移动图像
fixed_image = ants.image_read(args.fixed_image)
moving_image = ants.image_read(args.moving_image)

# 将变换应用到移动图像上
warped_image = ants.apply_transforms(fixed=fixed_image, moving=moving_image,
                                     transformlist=args.input_transform, imagetype=args.imagetype)

# 将结果保存为 NIfTI 格式文件
ants.image_write(warped_image, args.output_image)
