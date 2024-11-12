from autograd import grad
from cec2017.functions import f1, f2, f3
from booth import booth_function
from draw import *
from save import *
import constants


def find_min(function, beta, epsilon, arrow_color='b', max_iter=100, scale=True, dem_1=DEM_1, dem_2=DEM_2):
    x = np.random.uniform(-UPPER_BOUND, UPPER_BOUND, size=DIMENSIONALITY)
    prev_value = function(x)
    start_norm = 0
    i = 0
    for i in range(max_iter):
        x = np.clip(x, -100, 100)
        grad_fct = grad(function)
        gradient = grad_fct(x)

        current_norm = np.linalg.norm(gradient)
        if start_norm == 0:
            start_norm = current_norm

        if np.linalg.norm(gradient) < epsilon:
            print(f'Stopping criterion met (gradient norm < {epsilon}) at iteration {i}')
            break

        scale_factor = 1
        if scale:
            scale_factor = min(1, current_norm/start_norm)
        head_width = 2 * scale_factor
        head_length = 4 * scale_factor
        line_thickness = 1 * scale_factor

        plt.arrow(float(x[dem_1]), float(x[dem_2]), -gradient[dem_1] * beta, -gradient[dem_2] * beta,
                  head_width=head_width,
                  head_length=head_length,
                  linewidth=line_thickness, color=arrow_color)

        x = x - gradient * beta
        current_value = function(x)

        if abs(current_value - prev_value) < epsilon:
            print(f'Stopping criterion met (function value change < {epsilon}) at iteration {i}')
            break

        prev_value = current_value

        if np.any(np.isnan(x)):
            print(f'Warning: NaN encountered at iteration {i}')
            break

    if i == max_iter - 1:
        print(f'Maximum iterations reached ({max_iter}) without meeting stopping criteria.')
    return x


def main():
    func = f3
    setup_grid(func)
    beta = 0

    if func == f1:
        beta = 0.000000003
        #  For beta  [0, 0.00000003) convergent
        #  For beta >= 0.00000003 divergent
    elif func == f2:
        beta = 0.000000000000000006
    elif func == f3:
        beta = 0.0000000001
        # For beta [0, 0.00000001), the algorithm works effectively.
        # For beta >= 0.00000001, the algorithm diverges to infinity,
    elif func == booth_function:
        constants.DIMENSIONALITY = 2
        beta = 0.03

    minimums = []
    for index in range(len(COLORS)):
        color = COLORS[index % len(COLORS)]
        minimum = find_min(func, beta, 1e-3, arrow_color=color,scale=False)
        minimums.append(minimum)
        print(f'Iteration {index + 1}: Minimum is: {minimum} \nValue is: {func(minimum)}')

    minimums.sort(key=func)
    print(f"Absolute found minimum is : {minimums[0]} With value: {func(minimums[0])}")

    save_plot(func.__name__, beta=beta)
    plt.show()


if __name__ == '__main__':
    main()
