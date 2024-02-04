import os
import json
from pathlib import Path
from pydicom import dcmread
import shutil


def judge_config(scans_dir, config_json_file, task_name):
    if config_json_file.exists() is True:
        return 0
    else:
        dataset_description = dict()
        tmp = []
        num = 0
        for item in sorted(os.listdir(scans_dir)):
            count = 0
            dicom_dir = scans_dir / 'resources' / 'DICOM' / item
            if dicom_dir.exists() is False:
                dicom_dir = scans_dir / item
            for dicom in os.listdir(dicom_dir):
                if count == 0:
                    dicom_file = dicom_dir / dicom
                    dcm_info = dcmread(dicom_file, force=True)

                    SeriesDescription = dcm_info['SeriesDescription'].value
                    SeriesNumber = dcm_info['SeriesNumber'].value

                    if 'T1' in SeriesDescription:
                        info = {
                            "datatype": "anat",
                            "suffix": "T1w",
                            "criteria": {
                                "SeriesDescription": SeriesDescription,
                                "SeriesNumber": SeriesNumber
                            }
                        }
                        tmp.append(info)
                    elif 'BOLD' in SeriesDescription:
                        num += 1
                        info = {
                            "datatype": "func",
                            "suffix": "bold",
                            "custom_entities": f"task-{task_name}_run-0{num}",
                            "criteria": {
                                "SeriesDescription": SeriesDescription,
                                "SeriesNumber": SeriesNumber
                            }
                        }
                        tmp.append(info)
                    else:
                        info = {
                            "datatype": "",
                            "suffix": "",
                            "custom_entities": "",
                            "criteria": {
                                "SeriesDescription": SeriesDescription,
                                "SeriesNumber": SeriesNumber
                            }
                        }
                        tmp.append(info)
                    count = 1
                else:
                    break
        dataset_description["descriptions"] = tmp
        with open(config_json_file, 'w') as jf_config:
            json.dump(dataset_description, jf_config, indent=4)
        return 1


if __name__ == '__main__':
    scans_dir = Path('/mnt/ngshare2/to_them/me/pbfs2bids_test/test')  # dicom数据存放文件夹
    out_bids_path = '/mnt/ngshare2/to_them/me/pbfs2bids_test/bids'  # bids输出存放路径
    dataset = ''  # dataset名字 eg. PBFS
    subject = ''  # subject名字，不要有任何符号 eg. zhenyu
    session = ''  # session需要，直接写数字 eg. 01
    task_name = ''  # task的类型 eg. rest

    config_json_file = Path(f'{dataset}_config.json')
    order = judge_config(scans_dir, config_json_file, task_name)

    if order == 1:
        print(f'{dataset}_config.json 在当前文件夹下已生成，请自行进行自定义确认修改。')
    else:
        print('start dicom to bids')

        for dicom_dirname in os.listdir(scans_dir):
            dicom_dir = f'{scans_dir}/{dicom_dirname}'
            cmd = f'dcm2bids -d {dicom_dir} -p {subject} -s {session} -c {config_json_file} -o {out_bids_path}/{dataset}'
            os.system(cmd)

        dataset_description_file = os.path.join(out_bids_path, dataset, 'dataset_description.json')
        if not os.path.exists(dataset_description_file):
            dataset_description = dict()
            dataset_description['Name'] = f'{dataset}'
            dataset_description['BIDSVersion'] = '1.4.0'
            dataset_description['DatasetType'] = ''
            dataset_description['License'] = ''
            dataset_description['Authors'] = ['']
            dataset_description['HowToAcknowledge'] = ''
            dataset_description['Funding'] = ''
            dataset_description['ReferencesAndLinks'] = ['']
            dataset_description['DatasetDOI'] = ''

            with open(dataset_description_file, 'w') as jf:
                json.dump(dataset_description, jf, indent=4)

        shutil.rmtree(f'{out_bids_path}/{dataset}/tmp_dcm2bids')
