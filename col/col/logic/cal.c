/*
 * cal.c
 * Update Log:
 * 2018 / 11 / 29: 0.0.0
 * 实现函数的基本功能 主要的功能是在c语言中实现滤波器
 * 1. 
 * 1) filterCreateBandpass(b, a, order)
 * 2) filterCreateComb(b, a, order)
 * 3) filterCreateNotch(b, a, order)
 * 三个函数实现的功能是从python中传输IIR数字滤波器的参数，构造相关滤波器
 * 其中梳状陷波器 comb 的功能是滤除50Hz及其倍频的工频噪声
 * 显波器 notch 的功能是滤除60Hz的工频噪声
 * 因为这两个工频噪声不可能同时存在 所以数据在进入滤波器时仅仅可能过以上的某一个滤波器
 * 带通滤波器 bandpass 的功能是由用户选择的频带内进行带通滤波
 *    这里更好的方案是把16种可能的参数都提前算出来 然后在python中只要传参数就可以了
 *    这样好处是可以调整滤波器的阶数 达到绝对不会不稳定 精度和速度都最优的滤波器
 *    这个谁要做可以做一下啊 好麻烦啊 我肯定是不改了 
 *    如果这样的 还不如把32种滤波器都归纳成一个滤波器 这样运算量也很少 调用的包也少
 * 2.
 * 1) channelNumChange(int)
 * 2）indexInit(void)
 * 这两个函数就是初始化函数
 * channelNumChange 主要是初始化传入的通道数 
 * indexInit 这里主要是构造一个可以循环的链表 
 *    然后链表list终于实现了 发现好像还是用这种二维数组速度快一点
 *    其实链表list根本就没实现 c语言好麻烦啊 但是速度据说还是这个更快
 *    然后这个函数每次都要运行一次 因为每次都需要改以下当前最新值的位置
 *    肯定有更好的方案 不想再想了
 * 3.
 * 1) filter(char*)
 * 滤波器函数是现在最重要的函数 python中调用改函数得到滤波后的函数
 *    速度会快一些吧 如果不快的话 真的就炸了
 *    没有debug 需要构造数据 真是太麻烦了
 *    但是语法没有错吧 就先这样了
 *
 * by Zhao Zeming
 * 
 * 2018 / 12 / 2: 0.1.0
 * 在上次的功能上添加了新的功能 现在需要python程序中传送一个char型的指针即可
 * 本程序实现从char型的数组中找到肌电数据包并进行滤波 之后传送回python文件中
 * 增加的函数如下：
 * 1) splitPack2Filter(char*, int) 主要实现从python中提取数据到完成全部流程的主要函数，最后返回给python在这一组tcp包中有几组肌电完整包
 * 2) resultReturn(int) python从上一个函数得到值后 可以依次从该函数中得到所有已经滤波完成的值 
 *    以上功能经过最初的debug 基本功能完成 详细的边界的debug部分没有完成
 *
 * by Zhao Zeming
 */
#include <stdio.h>
#define BandpassMaxLen 30
#define CombMaxLen 50
#define NotchMaxLen 10
#define bool char
#define true 1
#define false 0

double bandpassA[BandpassMaxLen] = {0};
double bandpassB[BandpassMaxLen] = {0};
double combA[CombMaxLen] = {0};
double combB[CombMaxLen] = {0};
double notchA[NotchMaxLen] = {0};
double notchB[NotchMaxLen] = {0};

int dataCache[192] = {0};
double resCache[192] = {0};
double realResCache[50][192] = {0};
int resRes[2] = {0};

int combSrc[192][CombMaxLen] = {0};
int notchSrc[192][NotchMaxLen] = {0};
double bandpassSrc[192][BandpassMaxLen] = {0};

double combFit[192][CombMaxLen] = {0};
double notchFit[192][NotchMaxLen] = {0};
double bandpassFit[192][BandpassMaxLen] = {0};

unsigned char bandpassSrcIndex[BandpassMaxLen] = {0};
unsigned char combSrcIndex[CombMaxLen] = {0};
unsigned char notchSrcIndex[NotchMaxLen] = {0};

unsigned char notchSrcIndexFlag = 0;
unsigned char combSrcIndexFlag = 0;
unsigned char bandpassSrcIndexFlag = 0;

int bandpassLen = 0;
int combLen = 0;
int notchLen = 0;
int channelNum = 0;

int filterCreateBandpass(double*, double*, int);
int filterCreateComb(double*, double*, int);
int filterCreateNotch(double*, double*, int);
int channelNumChange(int);
double* filter(char*);
int indexInit(void);
int* splitPack2Filter(char*, int);
double* resultReturn(unsigned char);

int filterCreateBandpass(double* a, double *b, int nLen){
  bandpassLen = nLen;
  if (nLen){
    for(int i=0; i < bandpassLen; i++){
      bandpassA[i] = a[i];
      bandpassB[i] = b[i];
    }
  }
  else{
    for (int i=0; i < BandpassMaxLen; i++){
      bandpassA[i] = 0;
      bandpassB[i] = 0;
    }
  }
  return 0;
}
int filterCreateComb(double* a, double *b, int nLen){
  combLen = nLen;
  if (nLen){
    for(int i=0; i < combLen; i++){
      combA[i] = a[i];
      combB[i] = b[i];
    }
  }
  else{
    for(int i=0; i < CombMaxLen; i++){
      combA[i] = 0;
      combB[i] = 0;
    }
  }
  return 0;
}
int filterCreateNotch(double* a, double *b, int nLen){
  notchLen = nLen;
  if(nLen){
    for(int i=0; i < notchLen; i++){
      notchA[i] = a[i];
      notchB[i] = b[i];
    }
  }
  else{
    for (int i=0; i < NotchMaxLen; i++){
      notchA[i] = 0;
      notchB[i] = 0;
    }
  }
  return 0;
}
int channelNumChange(int a){
  channelNum = a;
  return 0;
}
double* filter(char* inputCache){
  int length = (int)(channelNum*1.5);
  int temp = 0;
  double tempData = 0;
  int powerFilterFlag = combLen + notchLen;
  char tempNum;
  unsigned char numTemp;
  for (int i=0; i < length; i++){
    switch(i % 3){
      case 0:
        dataCache[temp] = ((int)inputCache[0]) << 4;
        inputCache += 1;
        break;
      case 1:
        numTemp = (unsigned char)inputCache[0];
        dataCache[temp] |= numTemp >> 4;
        temp += 1;
        tempNum = inputCache[0] << 4;
        dataCache[temp] = ((int)(tempNum)) << 4;
        inputCache += 1;
        break;
      case 2:
        dataCache[temp] |= (unsigned char)inputCache[0];
        temp += 1;
        inputCache += 1;
        break;
    }
  }

  indexInit();
  for (int i=0; i < channelNum; i++){
    if (powerFilterFlag){
      if (combLen){
        combSrc[i][combSrcIndexFlag] = dataCache[i];
        tempData = combSrc[i][combSrcIndexFlag]*combB[0];
        for(int j=1; j < combLen; j++){
          tempData += (combSrc[i][combSrcIndex[j]]*combB[j] -
              combFit[i][combSrcIndex[j]]*combA[j]);
        }
        combFit[i][combSrcIndexFlag] = tempData;
      }
      else{
        notchSrc[i][notchSrcIndexFlag] = dataCache[i];
        tempData = notchSrc[i][notchSrcIndexFlag]*notchB[0];
        for(int j=1; j < notchLen; j++){
          tempData += (notchSrc[i][notchSrcIndex[j]]*notchB[j] -
              notchFit[i][notchSrcIndex[j]]*notchA[j]);
        }
        notchFit[i][notchSrcIndexFlag] = tempData;
      }
    }
    else{
      tempData = dataCache[i];
    }
    if (bandpassLen){
      bandpassSrc[i][bandpassSrcIndexFlag] = tempData;
      tempData = bandpassSrc[i][bandpassSrcIndexFlag]*bandpassB[0];
      for(int j=1; j < bandpassLen; j++){
        tempData += (bandpassSrc[i][bandpassSrcIndex[j]]*bandpassB[j] -
            bandpassFit[i][bandpassSrcIndex[j]]*bandpassA[j]);
      }
      bandpassFit[i][bandpassSrcIndexFlag] = tempData;
    }
    resCache[i] = tempData;
  }
  return resCache;
}
int indexInit(void){
  char temp;
  notchSrcIndexFlag += 1;
  if (notchSrcIndexFlag == NotchMaxLen){
    notchSrcIndexFlag = 0;
  }
  combSrcIndexFlag += 1;
  if (combSrcIndexFlag == CombMaxLen){
    combSrcIndexFlag = 0;
  }
  bandpassSrcIndexFlag += 1;
  if (bandpassSrcIndexFlag == BandpassMaxLen){
    bandpassSrcIndexFlag = 0;
  }
  notchSrcIndex[0] = notchSrcIndexFlag;
  combSrcIndex[0] = combSrcIndexFlag;
  bandpassSrcIndex[0] = bandpassSrcIndexFlag;
  temp = notchSrcIndexFlag;
  for (int i=1; i < notchLen; i++){
    if (temp == 0){
      temp = NotchMaxLen;
    }
    temp -= 1;
    notchSrcIndex[i] = temp;
    if (temp == 0){
      temp = NotchMaxLen;
    }
  }
  temp = combSrcIndexFlag;
  for (int i=1; i < combLen; i++){
    if (temp == 0){
      temp = CombMaxLen;
    }
    temp -= 1;
    combSrcIndex[i] = temp;
    if (temp == 0){
      temp = CombMaxLen;
    }
  }
  temp = bandpassSrcIndexFlag;
  for (int i=1; i < bandpassLen; i++){
    if (temp == 0){
      temp = BandpassMaxLen;
    }
    temp -= 1;
    bandpassSrcIndex[i] = temp;
    if (temp == 0){
      temp = BandpassMaxLen;
    }
  }
  return 0;
}
int* splitPack2Filter(char* cache, int nLen){
  int pointer = 0;
  unsigned char realResCacheIter = 0;
  char* tempPointer;
  int numMax = nLen - 2 - 1.5*channelNum;
  int dataLen = 1.5*channelNum;
  char judge = 0;
  int test;
  while (pointer < numMax){
    for(int i=pointer; i < numMax; i++){
      if (cache[i] == (char)0x55){
        if (cache[i + 1] == (char)0xAA){
          pointer = i + 2;
          break;
        }
      }
    }
    judge = 0;
    for (int i=pointer; i < pointer+dataLen; i++){
      judge += cache[i];
    }
    if (judge == cache[pointer + dataLen]){
      tempPointer = cache + pointer;
      filter(tempPointer);
      for (int i=0; i < channelNum; i++){
        realResCache[realResCacheIter][i] = resCache[i];
      }
      realResCacheIter += 1;
      pointer += (dataLen + 1);
    }
    else{
      pointer += 1;
    }
  }
  resRes[0] = realResCacheIter;
  resRes[1] = pointer;
  return resRes;
}
double* resultReturn(unsigned char num){
  return realResCache[num];
}