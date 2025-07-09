**## Detailed Description {#detailed-description .groupheader}**

The functions in this section use a so-called pinhole camera model. The

view of a scene is obtained by projecting a scene\'s 3D point $P_{w}$

into the image plane using a perspective transformation which forms the
coordinates, i.e. as 3D and 2D homogeneous vector respectively. You will

find a brief introduction to projective geometry, homogeneous vectors

and homogeneous transformations at the end of this section\'s

introduction. For more succinct notation, we often drop the

\'homogeneous\' and say vector instead of homogeneous vector.

The distortion-free projective transformation given by a pinhole camera

model is shown below.

$$
s\; p = A\begin{bmatrix}

{R|t}

\end{bmatrix}P_{w},
$$

where $P_{w}$ is a 3D point expressed with respect to the world

coordinate system, $p$ is a 2D pixel in the image plane, $A$ is the

camera [intrinsi] matrix, $R$ and $t$ are the rotation and translation that describe the

change of coordinates from world to camera coordinate systems (or camera

frame) and $s$ is the projective transformation\'s arbitrary scaling and

not part of the camera model.

The camera intrinsic matrix $A$ (notation used as in

[\[319\]](https://docs.opencv.org/4.11.0/d0/de3/citelist.html#CITEREF_zhang2000){.el}

and also generally notated as $K$) projects 3D points given in the

camera coordinate system to 2D pixel coordinates, i.e.

$$p = AP_{c}.$$

The camera intrinsic matrix $A$ is composed of the focal lengths $f_{x}$

and $f_{y}$, which are expressed in pixel units, and the principal point

$(c_{x},c_{y})$, that is usually close to the image center:

$$
A = \begin{bmatrix}

f_{x} & 0 & c_{x} \\

0 & f_{y} & c_{y} \\

0 & 0 & 1

\end{bmatrix},
$$

and thus

$$
s\begin{bmatrix}

u \\

v \\

1

\end{bmatrix} = \begin{bmatrix}

f_{x} & 0 & c_{x} \\

0 & f_{y} & c_{y} \\

0 & 0 & 1

\end{bmatrix}\begin{bmatrix}

X_{c} \\

Y_{c} \\

Z_{c}

\end{bmatrix}.
$$

The matrix of intrinsic parameters does not depend on the scene viewed.

So, once estimated, it can be re-used as long as the focal length is

fixed (in case of a zoom lens). Thus, if an image from the camera is

scaled by a factor, all of these parameters need to be scaled

(multiplied/divided, respectively) by the same factor.

The joint rotation-translation matrix $\lbrack R|t\rbrack$ is the matrix

product of a projective transformation and a homogeneous transformation.

The 3-by-4 projective transformation maps 3D points represented in

camera coordinates to 2D points in the image plane and represented in

normalized camera coordinates $x^{\prime} = X_{c}/Z_{c}$ and

$y^{\prime} = Y_{c}/Z_{c}$:

$$
Z_{c}\begin{bmatrix}

x^{\prime} \\

y^{\prime} \\

1

\end{bmatrix} = \begin{bmatrix}

1 & 0 & 0 & 0 \\

0 & 1 & 0 & 0 \\

0 & 0 & 1 & 0

\end{bmatrix}\begin{bmatrix}

X_{c} \\

Y_{c} \\

Z_{c} \\

1

\end{bmatrix}.
$$

The homogeneous transformation is encoded by the extrinsic parameters

$R$ and $t$ and represents the change of basis from world coordinate

system $w$ to the camera coordinate sytem $c$. Thus, given the

representation of the point $P$ in world coordinates, $P_{w}$, we obtain

$P$\'s representation in the camera coordinate system, $P_{c}$, by

$$
P_{c} = \begin{bmatrix}

R & t \\

0 & 1

\end{bmatrix}P_{w},
$$

This homogeneous transformation is composed out of $R$, a 3-by-3

rotation matrix, and $t$, a 3-by-1 translation vector:

$$
\begin{bmatrix}

R & t \\

0 & 1

\end{bmatrix} = \begin{bmatrix}

r_{11} & r_{12} & r_{13} & t_{x} \\

r_{21} & r_{22} & r_{23} & t_{y} \\

r_{31} & r_{32} & r_{33} & t_{z} \\

0 & 0 & 0 & 1

\end{bmatrix},
$$

and therefore

$$
\begin{bmatrix}

X_{c} \\

Y_{c} \\

Z_{c} \\

1

\end{bmatrix} = \begin{bmatrix}

r_{11} & r_{12} & r_{13} & t_{x} \\

r_{21} & r_{22} & r_{23} & t_{y} \\

r_{31} & r_{32} & r_{33} & t_{z} \\

0 & 0 & 0 & 1

\end{bmatrix}\begin{bmatrix}

X_{w} \\

Y_{w} \\

Z_{w} \\

1

\end{bmatrix}.
$$

Combining the projective transformation and the homogeneous

transformation, we obtain the projective transformation that maps 3D

points in world coordinates into 2D points in the image plane and in

normalized camera coordinates:

$$
Z_{c}\begin{bmatrix}

x^{\prime} \\

y^{\prime} \\

1

\end{bmatrix} = \begin{bmatrix}

{R|t}

\end{bmatrix}\begin{bmatrix}

X_{w} \\

Y_{w} \\

Z_{w} \\

1

\end{bmatrix} = \begin{bmatrix}

r_{11} & r_{12} & r_{13} & t_{x} \\

r_{21} & r_{22} & r_{23} & t_{y} \\

r_{31} & r_{32} & r_{33} & t_{z}

\end{bmatrix}\begin{bmatrix}

X_{w} \\

Y_{w} \\

Z_{w} \\

1

\end{bmatrix},
$$

with $x^{\prime} = X_{c}/Z_{c}$ and $y^{\prime} = Y_{c}/Z_{c}$. Putting

the equations for instrincs and extrinsics together, we can write out



$$
s\; p = A\begin{bmatrix}

{R|t}

\end{bmatrix}P_{w}
$$

 as
$$
s\begin{bmatrix}

u \\

v \\

1

\end{bmatrix} = \begin{bmatrix}

f_{x} & 0 & c_{x} \\

0 & f_{y} & c_{y} \\

0 & 0 & 1

\end{bmatrix}\begin{bmatrix}

r_{11} & r_{12} & r_{13} & t_{x} \\

r_{21} & r_{22} & r_{23} & t_{y} \\

r_{31} & r_{32} & r_{33} & t_{z}

\end{bmatrix}\begin{bmatrix}

X_{w} \\

Y_{w} \\

Z_{w} \\

1

\end{bmatrix}
$$

If $Z_{c} \neq 0$, the transformation above is equivalent to the

following,

$$
\begin{bmatrix}

u \\

v

\end{bmatrix} = \begin{bmatrix}

{f_{x}X_{c}/Z_{c} + c_{x}} \\

{f_{y}Y_{c}/Z_{c} + c_{y}}

\end{bmatrix}
$$


with

$$
\begin{bmatrix}

X_{c} \\

Y_{c} \\

Z_{c}

\end{bmatrix} = \begin{bmatrix}

{R|t}

\end{bmatrix}\begin{bmatrix}

X_{w} \\

Y_{w} \\

Z_{w} \\

1

\end{bmatrix}.
$$

The following figure illustrates the pinhole camera model.

::: {.image}

![](./OpenCV_%20Camera%20Calibration%20and%203D%20Reconstruction_files/pinhole_camera_model.png)

::: {.caption}

Pinhole camera model

:::

:::

Real lenses usually have some distortion, mostly radial distortion, and

slight tangential distortion. So, the above model is extended as:

$$
\begin{bmatrix}

u \\

v

\end{bmatrix} = \begin{bmatrix}

{f_{x}x^{''} + c_{x}} \\

{f_{y}y^{''} + c_{y}}

\end{bmatrix}
$$

where

$$
\begin{bmatrix}

x^{''} \\

y^{''}

\end{bmatrix} = \begin{bmatrix}

{x^{\prime}\frac{1 + k_{1}r^{2} + k_{2}r^{4} + k_{3}r^{6}}{1 + k_{4}r^{2} + k_{5}r^{4} + k_{6}r^{6}} + 2p_{1}x^{\prime}y^{\prime} + p_{2}(r^{2} + 2x^{\prime 2}) + s_{1}r^{2} + s_{2}r^{4}} \\

{y^{\prime}\frac{1 + k_{1}r^{2} + k_{2}r^{4} + k_{3}r^{6}}{1 + k_{4}r^{2} + k_{5}r^{4} + k_{6}r^{6}} + p_{1}(r^{2} + 2y^{\prime 2}) + 2p_{2}x^{\prime}y^{\prime} + s_{3}r^{2} + s_{4}r^{4}}

\end{bmatrix}
$$

with

$$
r^{2} = x^{\prime 2} + y^{\prime 2}
$$

and

$$
\begin{bmatrix}

x^{\prime} \\

y^{\prime}

\end{bmatrix} = \begin{bmatrix}

{X_{c}/Z_{c}} \\

{Y_{c}/Z_{c}}

\end{bmatrix},
$$

if $Z_{c} \neq 0$.

The distortion parameters are the radial coefficients $k_{1}$, $k_{2}$,

$k_{3}$, $k_{4}$, $k_{5}$, and $k_{6}$ , $p_{1}$ and $p_{2}$ are the

tangential distortion coefficients, and $s_{1}$, $s_{2}$, $s_{3}$, and

$s_{4}$, are the thin prism distortion coefficients. Higher-order

coefficients are not considered in OpenCV.

The next figures show two common types of radial distortion: barrel

distortion ( $1 + k_{1}r^{2} + k_{2}r^{4} + k_{3}r^{6}$ monotonically

decreasing) and pincushion distortion (

$1 + k_{1}r^{2} + k_{2}r^{4} + k_{3}r^{6}$ monotonically increasing).

Radial distortion is always monotonic for real lenses, and if the

estimator produces a non-monotonic result, this should be considered a

calibration failure. More generally, radial distortion must be monotonic

and the distortion function must be bijective. A failed estimation

result may look deceptively good near the image center but will work

poorly in e.g. AR/SFM applications. The optimization method used in

OpenCV camera calibration does not include these constraints as the

framework does not support the required integer programming and

polynomial inequalities. See [issue

\#15992](https://github.com/opencv/opencv/issues/15992){target="_blank"}

for additional information.

![](./OpenCV_%20Camera%20Calibration%20and%203D%20Reconstruction_files/distortion_examples.png){.inline}

![](./OpenCV_%20Camera%20Calibration%20and%203D%20Reconstruction_files/distortion_examples2.png){.inline}

In some cases, the image sensor may be tilted in order to focus an

oblique plane in front of the camera (Scheimpflug principle). This can

be useful for particle image velocimetry (PIV) or triangulation with a

laser fan. The tilt causes a perspective distortion of $x^{''}$ and

$y^{''}$. This distortion can be modeled in the following way, see e.g.

[\[171\]](https://docs.opencv.org/4.11.0/d0/de3/citelist.html#CITEREF_louhichi07){.el}.

$$
\begin{bmatrix}

u \\

v

\end{bmatrix} = \begin{bmatrix}

{f_{x}x^{'''} + c_{x}} \\

{f_{y}y^{'''} + c_{y}}

\end{bmatrix},
$$

where

$$
s\begin{bmatrix}

x^{'''} \\

y^{'''} \\

1

\end{bmatrix} = \begin{bmatrix}

{R_{33}(\tau_{x},\tau_{y})} & 0 & {- R_{13}(\tau_{x},\tau_{y})} \\

0 & {R_{33}(\tau_{x},\tau_{y})} & {- R_{23}(\tau_{x},\tau_{y})} \\

0 & 0 & 1

\end{bmatrix}R(\tau_{x},\tau_{y})\begin{bmatrix}

x^{''} \\

y^{''} \\

1

\end{bmatrix}
$$

and the matrix $R(\tau_{x},\tau_{y})$ is defined by two rotations with

angular parameter $\tau_{x}$ and $\tau_{y}$, respectively,

$$
R(\tau_{x},\tau_{y}) = \begin{bmatrix}

{\cos(\tau_{y})} & 0 & {- \sin(\tau_{y})} \\

0 & 1 & 0 \\

{\sin(\tau_{y})} & 0 & {\cos(\tau_{y})}

\end{bmatrix}\begin{bmatrix}

1 & 0 & 0 \\

0 & {\cos(\tau_{x})} & {\sin(\tau_{x})} \\

0 & {- \sin(\tau_{x})} & {\cos(\tau_{x})}

\end{bmatrix} = \begin{bmatrix}

{\cos(\tau_{y})} & {\sin(\tau_{y})\sin(\tau_{x})} & {- \sin(\tau_{y})\cos(\tau_{x})} \\

0 & {\cos(\tau_{x})} & {\sin(\tau_{x})} \\

{\sin(\tau_{y})} & {- \cos(\tau_{y})\sin(\tau_{x})} & {\cos(\tau_{y})\cos(\tau_{x})}

\end{bmatrix}.
$$

In the functions below the coefficients are passed or returned as

$$
(k_{1},k_{2},p_{1},p_{2}\lbrack,k_{3}\lbrack,k_{4},k_{5},k_{6}\lbrack,s_{1},s_{2},s_{3},s_{4}\lbrack,\tau_{x},\tau_{y}\rbrack\rbrack\rbrack\rbrack)
$$

vector. That is, if the vector contains four elements, it means that

$k_{3} = 0$ . The distortion coefficients do not depend on the scene

viewed. Thus, they also belong to the intrinsic camera parameters. And

they remain the same regardless of the captured image resolution. If,

for example, a camera has been calibrated on images of 320 x 240

resolution, absolutely the same distortion coefficients can be used for

640 x 480 images from the same camera while $f_{x}$, $f_{y}$, $c_{x}$,

and $c_{y}$ need to be scaled appropriately.

The functions below use the above model to do the following:

\- Project 3D points to the image plane given intrinsic and extrinsic

 parameters.

\- Compute extrinsic parameters given intrinsic parameters, a few 3D

 points, and their projections.

\- Estimate intrinsic and extrinsic camera parameters from several views

 of a known calibration pattern (every view is described by several

 3D-2D point correspondences).

\- Estimate the relative position and orientation of the stereo camera

 \"heads\" and compute the rectification\* transformation that makes

 the camera optical axes parallel.

***\*Homogeneous Coordinates\****  

Homogeneous Coordinates are a system of coordinates that are used in

projective geometry. Their use allows to represent points at infinity by

finite coordinates and simplifies formulas when compared to the

cartesian counterparts, e.g. they have the advantage that affine

transformations can be expressed as linear homogeneous transformation.

One obtains the homogeneous vector $P_{h}$ by appending a 1 along an

n-dimensional cartesian vector $P$ e.g. for a 3D cartesian vector the

mapping $P\rightarrow P_{h}$ is:


$$
\begin{bmatrix}

X \\

Y \\

Z

\end{bmatrix}\rightarrow\begin{bmatrix}

X \\

Y \\

Z \\

1

\end{bmatrix}.
$$

For the inverse mapping $P_{h}\rightarrow P$, one divides all elements

of the homogeneous vector by its last element, e.g. for a 3D homogeneous

vector one gets its 2D cartesian counterpart by:

$$
\begin{bmatrix}

X \\

Y \\

W

\end{bmatrix}\rightarrow\begin{bmatrix}

{X/W} \\

{Y/W}

\end{bmatrix},
$$


if $W \neq 0$.

Due to this mapping, all multiples $kP_{h}$, for $k \neq 0$, of a

homogeneous point represent the same point $P_{h}$. An intuitive

understanding of this property is that under a projective

transformation, all multiples of $P_{h}$ are mapped to the same point.

This is the physical observation one does for pinhole cameras, as all

points along a ray through the camera\'s pinhole are projected to the

same image point, e.g. all points along the red ray in the image of the

pinhole camera model above would be mapped to the same image coordinate.

This property is also the source for the scale ambiguity s in the

equation of the pinhole camera model.

As mentioned, by using homogeneous coordinates we can express any change

of basis parameterized by $R$ and $t$ as a linear transformation, e.g.

for the change of basis from coordinate system 0 to coordinate system 1

becomes:

$$
P_{1} = RP_{0} + t\rightarrow P_{h_{1}} = \begin{bmatrix}

R & t \\

0 & 1

\end{bmatrix}P_{h_{0}}.
$$


Note

:  - Many functions in this module take a camera intrinsic matrix as an

   input parameter. Although all functions assume the same structure

   of this parameter, they may name it differently. The parameter\'s

   description, however, will be clear in that a camera intrinsic

   matrix with the structure shown above is required.

  \- A calibration sample for 3 cameras in a horizontal position can be

   found at opencv_source_code/samples/cpp/3calibration.cpp

  \- A calibration sample based on a sequence of images can be found at

   opencv_source_code/samples/cpp/calibration.cpp

  \- A calibration sample in order to do 3D reconstruction can be found

   at opencv_source_code/samples/cpp/build3dmodel.cpp

  \- A calibration example on stereo calibration can be found at

   opencv_source_code/samples/cpp/stereo_calib.cpp

  \- A calibration example on stereo matching can be found at

   opencv_source_code/samples/cpp/stereo_match.cpp

  \- (Python) A camera calibration sample can be found at

   opencv_source_code/samples/python/calibrate.py
