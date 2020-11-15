# The L1 trend filtering - introduction.<br><br>
The problem of estimating underlying trends in time series data arises in a variety of disciplines. 
The ℓ1 trend filtering method produces trend estimates x that are piecewise linear from the time series y.

The ℓ1 trend estimation problem can be formulated as

$$
minimize \; (1/2) ||y-x||^2_2+λ||Dx||_1,
$$

with variable $x$, problem data $y$ and parameter $λ$, with $λ\geq0$

where D is the second difference matrix

$$
D = 
\begin{pmatrix}
1 & -2 & 1 & 0 & \cdots & 0 & 0 & 0 & 0\\
0 & 1 & -2 & 1 & \cdots & 0 & 0 & 0 & 0\\
& & & & \vdots  \\
0 & 0 & 0& 0 & \cdots & 1 & -2 & 1 & 0\\
0 & 0 & 0& 0 & \cdots & 0 & 1 & -2 & 1\\
\end{pmatrix}
$$

### Editable input parameters in the example: problem data $y$ and parameter $λ.$

## Example: L1 trend filtering for Bitcoin daily close.
![image](https://andreikeino.github.io/camex/images/console_output/L1_trend_filtering_bitcoin.png)

## The code and explanation are adopted from:
[https://www.cvxpy.org/examples/applications/l1_trend_filter.html](https://www.cvxpy.org/examples/applications/l1_trend_filter.html)
