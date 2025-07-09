# the **pinhole camera model** and its **intrinsic matrix**

Let’s begin with the heart of virtually every camera-based vision system: the **pinhole camera model** and its **intrinsic matrix**. We’ll break it down into bite-sized pieces.

------

## 1. The Pinhole Model Intuition

Imagine a dark box with a tiny hole (the “pinhole”) on one side and a film or sensor on the opposite side. Light rays from a 3D scene pass through the hole and project an upside-down image onto the sensor.

-   **No lenses**—just straight-line rays.
-   **Idealized**: no blur, no distortion.

This simple model lets us describe mathematically how a 3D point in space appears as a 2D point on our image.

------

## 2. Homogeneous Coordinates

To write projections neatly, we use **homogeneous coordinates**:

-   A 3D point $(X_c,\,Y_c,\,Z_c)$ in camera-space becomes $ [X_c,\;Y_c,\;Z_c,\;1]^\top$.
-   A 2D pixel $(u,\,v)$ becomes $ [u,\;v,\;1]^\top$.

Homogeneous vectors allow us to express translations and perspective with simple matrix multiplications.

------

## 3. From 3D Camera Coordinates to the Image Plane

First, assume our 3D world point $P_w$ has already been transformed into **camera coordinates** $P_c = [X_c,\,Y_c,\,Z_c]^\top$.

In an ideal pinhole:

$\begin{bmatrix} x'\\[4pt] y'\\[4pt] 1 \end{bmatrix} \;=\; \begin{bmatrix} X_c / Z_c \\[4pt] Y_c / Z_c \\[4pt] 1 \end{bmatrix}$

-   $x', y'$ are the **normalized image coordinates**.

-   Division by $Z_c$ accounts for the fact that farther points appear closer to the center.

------

## 4. Introducing the Intrinsic Matrix $A$

Normalized coordinates assume:

-   The pixel grid is 1 unit per “normalized” unit.
-   The optical center (principal point) is at $(0,0)$.

Real cameras have:

1.  **Focal lengths** $f_x, f_y$ (in pixels)—they scale normalized units to pixel units.
2.  **Principal point** $(c_x,\,c_y)$—the pixel coordinates of the optical axis’ intersection.

All of that packs into:

$A \;=\; \begin{bmatrix} f_x & 0   & c_x \\[4pt] 0   & f_y & c_y \\[4pt] 0   & 0   & 1 \end{bmatrix}$

------

## 5. Full Projection Equation

Putting it all together:

$s\; \underbrace{ \begin{bmatrix} u\\[4pt] v\\[4pt] 1 \end{bmatrix} }_{\text{pixel coords}} \;=\; A\, \underbrace{ \begin{bmatrix} X_c \\[4pt] Y_c \\[4pt] Z_c \end{bmatrix} }_{\substack{\text{3D point in} \\ \text{camera coords}}}$

Or, expanding:

$s \begin{bmatrix} u\\[4pt] v\\[4pt] 1 \end{bmatrix} = \begin{bmatrix} f_x & 0   & c_x \\[4pt] 0   & f_y & c_y \\[4pt] 0   & 0   & 1 \end{bmatrix} \begin{bmatrix} X_c \\[4pt] Y_c \\[4pt] Z_c \end{bmatrix} \quad\Longrightarrow\quad \begin{cases} u = \displaystyle \frac{f_x\,X_c}{Z_c} + c_x, \\[8pt] v = \displaystyle \frac{f_y\,Y_c}{Z_c} + c_y. \end{cases}$

-   The scalar $s$ cancels when we normalize back to $[u,v,1]^\top$.
-   s is the **projective scale factor**, and in pinhole cameras, it's equal to the **depth $Z_c$** in the camera frame.
-   Intuitively, $\tfrac{X_c}{Z_c}$ and $\tfrac{Y_c}{Z_c}$ “flatten” depth, then $f$ scales, and $c$ shifts.

------

## 6. A Numerical Example

Say your camera has:

-   $f_x = 800$, $f_y = 800$ (square pixels),
-   Principal point $(c_x,c_y) = (320,240)$.

A 3D point in camera coords is $(X_c, Y_c, Z_c) = (0.1,\,0.05,\,2.0)$ m.

1.  Compute normalized:

    $x′=0.1/2.0=0.05,y′=0.05/2.0=0.025.x' = 0.1/2.0 = 0.05,\quad y' = 0.05/2.0 = 0.025$.

2.  Pixel:

    $u=800⋅0.05+320=40+320=360,v=800⋅0.025+240=20+240=260.u = 800\cdot0.05 + 320 = 40 + 320 = 360,  \quad v = 800\cdot0.025 + 240 = 20 + 240 = 260$

So that 3D point appears at pixel $(360,\,260)$.

------

### ✅ Recap

1.  **Pinhole “flattens”** 3D rays to 2D via division by depth.

2.  **Intrinsic** scale ($f_x,f_y$) and shift ($c_x,c_y$) normalized coords into pixel coords.

3.  **Key equation**:
    $$
    \begin{bmatrix}u\\v\end{bmatrix} =  \begin{bmatrix} f_x\,\dfrac{X_c}{Z_c} + c_x \\[4pt] f_y\,\dfrac{Y_c}{Z_c} + c_y \end{bmatrix}.
    $$
    

------

#### What next?

-   **Extrinsics** $[R\mid t]$: how to go from world coordinates $P_w$ to camera coordinates $P_c$.
-   the **pinhole camera model** and its **intrinsic matrix**
-   **Lens distortion**: real lenses deviate from ideal pinhole.

Let me know which you’d like to explore next!

Great question — the **$s$** in the camera projection equation is very important and often misunderstood.

------

## 📌 Equation:

$s \cdot \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = A \cdot [R \mid t] \cdot \begin{bmatrix} X_w \\ Y_w \\ Z_w \\ 1 \end{bmatrix}$

Where:

-   $(X_w, Y_w, Z_w)$: 3D world coordinates
-   $(u, v)$: image pixel coordinates
-   $A$: intrinsic matrix
-   $[R \mid t]$: extrinsic transformation
-   **$s$**: scale factor

------

## 🧮 What is $s$? (Short Answer)

**$s$ is the depth (Z value) in camera coordinates:**

$s = Z_c$

It ensures the equation uses **homogeneous coordinates** correctly.

------

## 🧠 Why Do We Need It?

In projective geometry, we use **homogeneous coordinates**, which allow us to represent points like this:

$p = \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} \quad \text{actually means} \quad \lambda \cdot \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} \quad \text{for any } \lambda \ne 0$

So after applying the camera matrix and projection, the resulting 3D vector needs to be scaled to get back to the normalized pixel format (where the third coordinate is 1). That’s what $s$ does.

------

## ✅ Example

Imagine a point in camera coordinates is:

$P_c = \begin{bmatrix} X_c \\ Y_c \\ Z_c \end{bmatrix}$

We apply the intrinsic matrix:

$A \cdot P_c =  \begin{bmatrix} f_x X_c + c_x Z_c \\ f_y Y_c + c_y Z_c \\ Z_c \end{bmatrix}$

Then:

$s \cdot  \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \begin{bmatrix} f_x X_c + c_x Z_c \\ f_y Y_c + c_y Z_c \\ Z_c \end{bmatrix}$

So you divide by $Z_c$ (that’s your $s$) to get the final image coordinates:

$u = \frac{f_x X_c}{Z_c} + c_x,\quad v = \frac{f_y Y_c}{Z_c} + c_y$

------

## ✅ Summary

-   $s$ is the **projective scale factor**, and in pinhole cameras, it's equal to the **depth $Z_c$** in the camera frame.
-   It ensures correct scaling in homogeneous coordinates.
-   You usually eliminate it by dividing through during projection.

------

Would you like to go through an example using actual numbers to see how $s$ behaves?