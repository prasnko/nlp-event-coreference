'''
Created on Dec 5, 2012

@author: jasonleakey
'''
from core import *
import xml.etree.cElementTree as ET
from types import NoneType

class Frame():
    def __init__(self):
        self._frame_name = ''
        self._target = ''
        self._frame_elems = {}
        pass

    def get_frame_name(self):
        return self._frame_name

    def set_frame_name(self, name):
        self._frame_name = name

    def get_target(self):
        return self._target

    def set_target(self, target):
        self._target = target

    def get_all_frame_elems(self):
        return self._frame_elems

    def set_frame_elems(self, fnelems):
        self._frame_elems = fnelems

    def add_frame_elem(self, fn_elem):
        self._frame_elems.update(fn_elem)

    def __str__(self):
        return 'FrameName: ' + self._frame_name + \
            'Target: ' + self._target + \
            'FrameElems: ' + self._frame_elems

class FrameNetFeatureExtractor(FeatureExtractorBase):
    def __init__(self):
        self._xml_path = '../res/bigfile.xml'
        self._index_path = '../res/index_bigfile'
        self._frame_cache = {}
        self._load_index()
        self._load_xml()

    def extract(self, em1, em2):
#        print em1.get_sent().whereis()
        features = {}
        frame_list_1 = self._get_frames(em1.get_sent().whereis())
        frame_list_2 = self._get_frames(em2.get_sent().whereis())

        frame1 = self._match_frame(frame_list_1, em1)
        frame2 = self._match_frame(frame_list_2, em2)

        if isinstance(frame1, Frame) and isinstance(frame2, Frame) and not cmp(frame1.get_frame_name(), frame2.get_frame_name()):
            features['FrameNameSim'] = 1
        else:
            features['FrameNameSim'] = 0

        if isinstance(frame1, Frame) and isinstance(frame2, Frame):
            set_A = set(frame1.get_all_frame_elems().keys())
            set_B = set(frame2.get_all_frame_elems().keys())
            if len(set_A) == 0 or len(set_B) == 0:
                features['FE_Sim'] = 0
            else:
                common_elem = len(set_A & set_B)
                # Dice's coefficient similarity
                features['FE_Sim'] = 1.0 * 2 * common_elem / (len(set_A) + len(set_B))
        else:
            features['FE_Sim'] = 0

        return features

    def _match_frame(self, frame_list, em):
        for frame in frame_list:
            if not cmp(em.get_mention(), frame.get_target()):
                return frame
        return NoneType


    def _get_frames(self, loc):
        idx = self._get_idx(loc)
#        print loc, ',', idx
        if self._frame_cache.has_key(idx):
            return self._frame_cache[idx]

        sent_elem = self._xml.find('.//sentence[@ID="' + str(idx) + '"]')
        sent_text = sent_elem.find('./text').text
#        print 'Sentence: ' + sent_text
        frames = []
        for annot in sent_elem.findall('.//annotationSet'):
#            print 'FrameName:' + annot.get('frameName')
            frame = Frame()
            frame.set_frame_name(annot.get('frameName'))

            target_layer = annot.find('.//layer[@name="Target"]')
            target_label = target_layer.find('.//label')
            target = sent_text[int(target_label.get('start')) : int(target_label.get('end')) + 1]
#            print 'Target: ' + target
            frame.set_target(target)

            FE = annot.find('.//layer[@name="FE"]')
            FE_labels = FE.findall('.//label')
#            print 'Frame Elements: ',
            for fe_label in FE_labels:
                fe_text = sent_text[int(fe_label.get('start')) : int(fe_label.get('end')) + 1]
                fe_role = fe_label.get('name')
#                print {fe_role: fe_text},
                frame.add_frame_elem({fe_role : fe_text})

            frames.append(frame)
        # ## cache frame
        self._frame_cache[idx] = frames
#        print frames
        return frames

    def _get_idx(self, tuple):
        return self._idx_map.get(tuple)

    def _load_index(self):
        '''
        load the index_bigfile 
        '''
        index_file = open(self._index_path)
        self._idx_map = {}
        for line in index_file:
            tmp = line.split(' ')
            self._idx_map[tuple([int(tmp[0]), int(tmp[1]), int(tmp[2])])] = int(tmp[3])
        index_file.close()

    def _load_xml(self):
        tree = ET.parse(self._xml_path)
        self._xml = tree.getroot()

    def get_features(self):
        return self._feature_table

if __name__ == '__main__':
    ft_ext_list = [FrameNetFeatureExtractor()]
#
    engine = MainEngine(ft_ext_list)
    engine.run_within_doc()
    engine.save_within_feature('fn_within_features.txt')
    engine.run_cross_doc()
    engine.save_cross_feature('fn_cross_features.txt')

#    FrameNetFeatureExtractor().extract(1, 2)
