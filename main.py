from data_preprocessing import *
from metric import *
from models import *
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='experiment settings')
    parser.add_argument('--cuda_idx', type=int, nargs='?', default=0, help='device index')
    parser.add_argument('--window_size', type=int, nargs='?', default=10, help='length of sequence')
    parser.add_argument('--total_num', type=int, nargs='?', default=5, help='number of examples for each task')
    parser.add_argument('--isruc1_path', type=str, nargs='?',
                        default='/home/ShareData/ISRUC-1/ISRUC-1', help='file path of isruc1 dataset')
    parser.add_argument('--isruc1', nargs='+', default=['C4_A1', 'LOC_A2'], help='channels for isruc1')
    parser.add_argument('--shhs_path', type=str, nargs='?',
                        default='/home/ShareData/shhs1_process6', help='file path of shhs dataset')
    parser.add_argument('--shhs', nargs='+', default=['EEG', 'EOG(L)'], help='channels for shhs')
    parser.add_argument('--mass_path', type=str, nargs='?',
                        default='/home/ShareData/MASS_SS3_3000_25C-Cz', help='file path of mass dataset')
    parser.add_argument('--mass', nargs='+', default=['C4', 'EogL'], help='channels for mass')
    parser.add_argument('--sleep_edf_path', type=str, nargs='?',
                        default='/home/ShareData/sleep-edf-153-3chs', help='file path of sleepedf dataset')
    parser.add_argument('--sleep_edf', nargs='+', default=['Fpz-Cz', 'EOG'], help='channels of sleepedf')
    parser.add_argument('--task_num', type=int, nargs='?', default=4, help='number of tasks')
    args = parser.parse_args()
    device = torch.device(f'cuda:{args.cuda_idx}')
    datas, labels = load_all_datasets(args)
    trains, valids, tests = create_fold_task_separated([0, 1, 2], [3], [4], datas, labels)
    net = SeqSleepNet()
    net.apply(init_weight)
    net.to(device)
    confusion_maxtrix = ConfusionMatrix(4, 5)
    print(confusion_maxtrix.mat)
    confusion_maxtrix = evaluate_tasks(net, tests, confusion_maxtrix, device)
    print(confusion_maxtrix.mat)
