import os
from fontTools.ttLib import TTFont
import matplotlib.font_manager
import re
import json
import pickle
import config

# Windows/Fonts
# AppData/Local/Microsoft/Windows/Fonts ??
# AppData/Roaming/Microsoft/Windows/Fonts 不存在
# 注册表
# Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders 非
# SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts
# SOFTWARE\Microsoft\Windows\CurrentVersion\Fonts 不存在

class MyFontGroup:
    '''
    fontTable: dict(ftname: {Path:, IsInstalled:, Forced:, Tag: list})
    dupTable: dict(ftname: [dict, dict, ...])
    '''
    def __init__(self) -> None:
        # ttf, otf, ttc
        self.installedFontList = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

        self.ignList = [] # paths
        self.dupTable = {} # paths
        self.fontTable = {}        

    def __import_from_file(self, path):
        file = re.sub('/', r'\\', path)
        if re.search('\.(ttf|otf|ttc)$', file, flags=re.I)!=None:
            ft = TTFont(file, lazy=True, fontNumber=0)
            ftname = ft['name']
            for langID in config.fontIDSeq:
                try:
                    fname = ftname.getName(nameID=1, platformID=3, platEncID=1, langID=langID)
                    fstyle = ftname.getName(nameID=2, platformID=3, platEncID=1, langID=langID)
                    fontname = fname.toStr() + ' ' + fstyle.toStr()
                    if fontname not in self.fontTable.keys():
                        self.fontTable[fontname] = {'Path': file, 
                                                    'Forced': False, 
                                                    'IsInstalled': file in self.installedFontList,
                                                    'Tag': ['new']}
                        break
                    else: # dup
                        print ('Dupe: {}'.format(file))
                        if fontname in self.dupTable.keys():
                            self.dupTable[fontname].append({'Path': file, 'IsInstalled': file in self.installedFontList})
                        else:
                            self.dupTable[fontname] = [{'Path': file, 'IsInstalled': file in self.installedFontList}, 
                                                       {'Path': self.fontTable[fontname]['Path'], 'IsInstalled': file in self.installedFontList}]
                        break
                except:
                    pass
            else:
                print ('Ignore: {}'.format(file))
                self.ignList.append(file)
        else:
            print ('Ignore: {}'.format(file))
            self.ignList.append(file)

    def import_from_folder(self, path):
        for rootPath, dirs, files in os.walk(path):
            for file in files:
                if re.search('\.(fon|ttf|ttc|otf|afm|eof|woff)$', file, flags=re.I)!=None:
                    file = os.path.join(rootPath, file)
                    self.__import_from_file(file)
    
    def import_from_files(self, pathList):
        for path in pathList:
            if re.search('\.(fon|ttf|ttc|otf|afm|eof|woff)$', path, flags=re.I)!=None:
                self.__import_from_file(path)
    
    def import_from_conf(self):
        with open('data/fonttable.pickle', 'rb') as file:
            self.fontTable = pickle.load(file)
        with open('data/duptable.pickle', 'rb') as file:
            self.dupTable = pickle.load(file)


    def add_tag(self, fonts, tags):
        for ft in fonts:
            font = self.fontTable[ft]
            font['Tag'] = list(set(font['Tag']).union(tags))
            self.fontTable[ft] = font

    def remove_tag(self, fonts, tags):
        for ft in fonts:
            font = self.fontTable[ft]
            font['Tag'] = list(set(font['Tag']).difference(tags))
            self.fontTable[ft] = font

    def set_tag(self, fonts, tags):
        for ft in fonts:
            self.fontTable[ft]['Tag'] = tags

    def scan(self):
        self.installedFontList = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        # fontTable
        delList = []
        for k,v in self.fontTable.items():
            if os.path.exists(v['Path'])==False:
                delList.append(k)
                continue
            if v['Forced']==True: continue
            self.fontTable[k]['IsInstalled'] = v['Path'] in self.installedFontList
        for k in delList:
            del self.fontTable[k]
        # dupTable
        tmpTable = {}
        for k,v in self.dupTable.items(): # v: List
            tmp = []
            for vi in v:
                if os.path.exists(vi['Path'])==False:
                    continue
                tmp.append({'Path': vi['Path'], 'IsInstalled': vi['Path'] in self.installedFontList})
            if len(tmp)>=2:
                tmpTable[k] = tmp
        self.dupTable = tmpTable


    def font_count(self):
        return len(self.fontTable)

    def tag_count(self, tag):
        count = 0
        for i in self.fontTable.values():
            if tag in i['tag']: count += 1
        return count


    def export_fonttable(self):
        with open('data/fonttable.pickle', 'wb') as tmp:
            pickle.dump(self.fontTable, tmp)

    def export_duptable(self):
        with open('data/duptable.pickle', 'wb') as tmp:
            pickle.dump(self.dupTable, tmp)

    def export_ignList(self):
        if os.path.exists('data/ignfontlist.json')==True:
            with open('data/ignfontlist.json', 'w') as f:
                tmp = json.load(f)
                self.ignList = list(set(self.ignList).union(tmp))
        with open('data/ignfontlist.json', 'w') as f:
            json.dump(self.ignList, f)

