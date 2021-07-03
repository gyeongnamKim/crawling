import pandas as pd
import numpy as np

#파일 읽어오기
graduates_data = pd.read_excel('./2016_middle_shcool_graduates_report.xlsx')
del graduates_data['Unnamed: 0']
#행,열 이름 출력하기
print(graduates_data.index)
print(graduates_data.columns)

#자료형 확인하기
print(graduates_data.info())

# 데이터 통계 요약정보 확인하기
print(graduates_data.describe())

#구별 진학률 구하기
graduates_data['진학률'] = np.sum(graduates_data.iloc[:,7:16],axis=1)
graduates_data['진학률'] = graduates_data['진학률'].apply(lambda x:1 if x > 1 else x)
graduates_gu = graduates_data.groupby('지역')['진학률'].mean()
print(graduates_gu)