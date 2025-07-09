# PID 算法介绍

>   参考的优秀资源:
>
>   [PID算法(1) PID算法的原理推导_pid公式推导过程-CSDN博客](https://blog.csdn.net/mayuxin1314/article/details/135380335?spm=1001.2014.3001.5502)
>
>   [【中科大RM电控合集】PID算法纯意识流教学_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Uh4y1f7cL/?spm_id_from=333.788.videopod.sections&vd_source=b710c0374cb950d2cc5713ef9df39177)

### 1.PID的目标和框架

我们想要在错综复杂的物理世界中控制一个量(被控系统的状态),使得它达到目标值.

根据可能得控制方式,建立模型:

![image-20250427113446574](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427113446574.png)

可以认为:控制器的控制量和执行机构的动作之间的关系是确定的映射:
$$
Force_{control} = F({control\ signal})
$$
其中$Force_{control}$是我们为了控制被控系统,所给的外力(控制作用); control signal是控制器给的一个控制信号.

可以这么理解:电脑(控制器)经过运算,给了电机(执行机构)一个电流,电机输出外力,控制汽车(被控系统)的速度.

此外,控制信息就是目标值(target);也就是我们想要的系统状态(以要求的速度行驶).

那么为什么要闭环系统?

这是因为,客观的物理世界中,被控系统的响应是复杂的: 考虑一个State
$$
\Delta{State_{sys}} = \Phi[Force + f(state,environment)]*\Delta{t}
$$
其中系统状态的改变是由我给的外力和一个响应产生的阻力造成的.

设想我们要让火箭以给定的运动轨迹升空.这个阻力可以是主动的(不加外力也有,比如重力),被动的(空气阻力);

其中这个合力与State变化的mapping relationship应该是由一个函数$\Phi$决定的.

由这个响应关系,我们不难发现我们的控制逻辑:

-   1.让这个$\Phi$尽可能简单-能像牛二定律这样的单调线性函数,最好.
-   2.考虑我们最终的稳态:State = target. 从而 $f$ 给定(假设环境也不变);从而Force一定是确定的,与f项抵消.
-   3.怎么在不知道 $f$ 表达式的情况下,如果用开环控制,你没法直接给出控制Force的值.(你并不知道你该怎么控制去抵消f影响)
-   4.就算f不知道表达式,我们依旧要从f的实时数据中找到控制的Force该怎么取.

根据第四点和第二点:我们的控制思路有了:

>   **考虑$Error = Target - CurrentState $** 我们根据这个偏差, 给出控制的外力F:
>
>   要求Error越大,控制作用的F的值就越大,这可以使得$\Delta{State}$这个增量大,尽快减小error
>
>   要求逐步找到 $f(Target,environment)$也就是F的最终稳态值.

于是,我们给出一个反馈的模型—闭环模型的specific version:

![image-20250427141616179](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427141616179.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b74abc309fa31f8c9fa6c090d285d93f.png)

教科书上面的公式
$$
u_t=K_P*e_t+{K_i}\int^t_0e_{t}dt+K_d\frac{de_{t}}{dt}
$$
<img src="C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427142043098.png" alt="image-20250427142043098" style="zoom:50%;" />

也即
$$
u_{out}=P_{out}+I_{out}+D_{out}
$$

###2.对于PID每一项的理解

1.   误差的定义:记设定值目标为$s_t$ ;则误差是设定值与观测值之差:$e_t = s_t - x_t$

2.   $Kp, Ki,Kd$都是实际中自己调节出来的参数.

####比例项: Proportion

$$
P_{out} = K_pe_t
$$

![image-20250427143335666](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427143335666.png)
>用一个RL电路做理解:电流被电阻的输出给调节了.一开始电流大,电流衰减也快;
>
>电流曲线会像一个衰减的指数函数,归于稳态i = 0.(此处,$f$这个干扰项我忽略了)
>
>当然实际中,由于控制是离散的,只要Kp够大,也会震荡.

仿真:

![image-20250427144314803](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427144314803.png)

![image-20250427144400474](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427144400474.png)

#### 积分项

$$
S_t = e_1+e_2+e_3 + \dots +e_t
$$

![image-20250427144605175](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427144605175.png)

#### 微分项

误差的微分就是误差的变化速率，误差变化越快，其微分绝对值越大。误差增大时，其微分为正；误差减小时，其微分为负。控制器输出量的微分部分与误差的微分成正比，反映了被控量变化的趋势;作用是:**当偏差变化过快，从上次采样到当前采样的这段时间被控制对象的状态变化趋势，这种变化的趋势很可能会在一定程度上延续到下一个采样时间点，微分环节会输出较大的负数，作为抑制输出继续上升，提前控制抑制过冲。**

------------------------------------------------

而在实践中,我们在连续的物理世界建立离散化模型:

​	每隔$\Delta{t}$采样Error,有

![image-20250427145326888](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427145326888.png)

### 3.常见算法拓展

>   积分分离:

需要一个 𝑒𝑟𝑟𝑜𝑟𝑖分离阈值参数 𝑑
当 𝑒𝑟𝑟𝑜𝑟𝑖大于某给定值 𝑑时， $error_i$和 𝐼𝑖保持为 0 不参与计算
防止积分过大导致严重超调问题.举例,电机卡住了,$I_i$一直变大,输出控制驱动的电流一直增加

>变速积分:

𝑒𝑟𝑟𝑜𝑟𝑎𝑙𝑙𝑖需要额外乘一个系数 𝑘
当 𝑒𝑟𝑟𝑜𝑟𝑖绝对值大于某给定值 𝐵时， 𝑘=0
当 𝑒𝑟𝑟𝑜𝑟𝑖绝对值小于某给定值 𝐴时， 𝑘=1
当 𝑒𝑟𝑟𝑜𝑟𝑖绝对值在 𝐴,𝐵时， 𝑘以某种函数形式从 1 减小到 0 ，一般情况下线性函数即可
防止积分过大导致严重超调问题

![image-20250427145712153](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427145712153.png)

>   微分先行:

把原本 𝑒𝑟𝑟𝑜𝑟𝑖的差值变成当前值 𝑛𝑜𝑤𝑖的反向差值
𝐷𝑖=−𝑘𝑑∗(𝑛𝑜𝑤𝑖−𝑛𝑜𝑤𝑖−1)
**加快**(而不是减慢)系统响应速度，避免过度提前预判导致减速
适合于给定指令频繁升降的场合，可以避免指令的改变导致超调过大

>   输出限幅:

需要一个幅度限制参量 𝑐
当 输出值绝对值超出某给定值 𝑐时，绝对值恒等于 𝑐
一定程度上防止输出过高损坏设备，也算尊重现实

>   多环PID

$大环套小环.为了让前面提过的映射\Phi是简单的,可以理解的$

举例:控制位置:先用PID从驱动力F控制速度-再由PID用速度控制位移.这里是电机转角(进一步有齿轮带动整体前进)

![image-20250427150303468](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427150303468.png)

![image-20250427150315215](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427150315215.png)

>   前馈算法

前馈算法

>   •  想象你在练习唱歌 当你唱了几遍，有点印象，或者再多练习直至完全熟悉的时候;大概率自己能唱下来了，一些地方稍微看看谱子就能顺下去
>   •  在当前值、目标值之外，PID系统又输入了一个抽象的值
>   •  这个值是你通过唱了几遍熟能生巧后掌握的知识,这个知识是通过其他途径输入到系统中的，但与输入有关，那不妨就叫做前馈吧.

简单来说,就是你从之前输入掌握了输入变化的规律.可以预测之后可能的输入了.**离散前馈算法主要用于提升系统对设定值变化的响应速度和控制精度**

具体来说,就是用泰勒展开来预测函数.

![泰勒展开逼近图片 的图像结果](https://tse1-mm.cn.bing.net/th/id/OIP-C.wsrjyTpGzdphVWDD6SZkrwHaEn?w=264&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7)

假设你要估计$e^x$在0处之后的函数值,但是你只有零之前的数据.

怎么办?talyor expansion 告诉我们由与这个点相切的切线,抛物线,三次曲线就可以推出原函数.我们需要的只是不同阶的导数.而由差分法可以近似求得导数.(这个图片是不必要的)利用它,我们去预测$\delta t$时刻的输入,从而调整控制量.

![img](https://bkimg.cdn.bcebos.com/formula/8e916fa2c76aef2f90a408d6d3206eaa.svg)

####离散前馈算法公式

设 $r(k)$ 是离散时刻 $k$ 的设定值，$y(k)$ 是离散时刻 $k$ 的被控变量，$u(k)$ 是离散时刻 $k$ 的控制量。二阶前馈控制项 $u_{ff}(k)$ 结合PID反馈控制 $u_{fb}(k)$ 得到总控制量 $u(k)$，即：

$$
u(k)=u_{ff}(k)+u_{fb}(k)
$$

1. 一阶差分和二阶差分计算

• 一阶差分 $\Delta r(k)$ 表示设定值的一阶变化率，公式为：


$$
\Delta r(k)=r(k)-r(k - 1)
$$

• 二阶差分 $\Delta^2 r(k)$ 表示设定值的二阶变化率，公式为：


$$
\Delta^2 r(k)=\Delta r(k)-\Delta r(k - 1)=[r(k)-r(k - 1)]-[r(k - 1)-r(k - 2)]=r(k)-2r(k - 1)+r(k - 2)
$$

2. 二阶前馈控制项公式

二阶前馈控制项 $u_{ff}(k)$ 一般形式为：

$$
u_{ff}(k)=K_1\Delta r(k)+K_2\Delta^2 r(k)
$$

其中 $K_1$ 是一阶前馈增益，$K_2$ 是二阶前馈增益，这两个增益需要根据被控对象的特性进行整定。

3. PID反馈控制项公式

PID反馈控制项 $u_{fb}(k)$ 的离散公式通常采用位置式PID算法，表达式为：

$$
u_{fb}(k)=K_p e(k)+K_i\sum_{i = 0}^{k}e(i)+K_d[e(k)-e(k - 1)]
$$

其中 $K_p$ 是比例系数，$K_i$ 是积分系数，$K_d$ 是微分系数，$e(k)=r(k)-y(k)$ 是离散时刻 $k$ 的误差。

4. 总控制量公式

总控制量 $u(k)$ 是二阶前馈控制项和PID反馈控制项之和，即：

$$
u(k)=K_1\Delta r(k)+K_2\Delta^2 r(k)+K_p e(k)+K_i\sum_{i = 0}^{k}e(i)+K_d[e(k)-e(k - 1)]
$$

>   对于电机,可以这么形象理解
>   ![image-20250427151717876](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427151717876.png)

PID+Feedforward ，前馈-一阶就足够的差分预测模式
•感性认知：目标变化越剧烈，我给的提前量预判越多
•$𝑒𝑟𝑟𝑜𝑟_{𝑡𝑎𝑟𝑔𝑒𝑡𝑖}=𝑡𝑎𝑟𝑔𝑒𝑡_𝑖−𝑡𝑎𝑟𝑔𝑒𝑡_{𝑖−1}$
•$𝐹𝑖$=$𝑘_𝑓$∗$𝑒𝑟𝑟𝑜𝑟_{𝑡𝑎𝑟𝑔𝑒𝑡𝑖}$
•𝑘𝑓是前馈系数，是控制器的参数;大小需要手动调节，根据现实情况来调

![image-20250427152316391](C:\Users\Xujiaming\AppData\Roaming\Typora\typora-user-images\image-20250427152316391.png)

