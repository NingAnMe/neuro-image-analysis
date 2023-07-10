import argparse
import ants
"""reference
https://antspy.readthedocs.io/en/latest/registration.html

python ants_apply_transforms.py --moving_image moving_image.nii.gz --fixed_image fixed_image.nii.gz --output_image output_image.nii.gz --input_transform transform.mat transform1.mat 
"""

# 创建一个命令行解析器
parser = argparse.ArgumentParser(description='ANTS registration script')

# 添加需要的命令行参数
parser.add_argument('--moving_image', type=str, help='path to moving image')
parser.add_argument('--fixed_image', type=str, help='path to fixed image')
parser.add_argument('--output_image', type=str, help='path to output image')
parser.add_argument('--input_transform', type=str, nargs='+', default=['transform.mat'],
                    help='path to input transform files')

# 解析命令行参数
args = parser.parse_args()

# 读取固定图像和移动图像
fixed_image = ants.image_read(args.fixed_image)
moving_image = ants.image_read(args.moving_image)

# 将变换应用到移动图像上
warped_image = ants.apply_transforms(fixed=fixed_image, moving=moving_image,
                                     transformlist=args.input_transform)

# 将结果保存为 NIfTI 格式文件
ants.image_write(warped_image, args.output_image)
