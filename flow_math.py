import numpy as np

def source_sink(strength, x_source, y_source, X, Y):
    dx = X - x_source
    dy = Y - y_source
    r2 = dx**2 + dy**2
    u = strength / (2 * np.pi) * dx / r2
    v = strength / (2 * np.pi) * dy / r2
    return u, v

def uniform_flow(U, X, Y):
    u = U * np.ones_like(X)
    v = np.zeros_like(Y)
    return u, v

def vortex(strength, x_vortex, y_vortex, X, Y):
    dx = X - x_vortex
    dy = Y - y_vortex
    r2 = dx**2 + dy**2
    u = -strength / (2 * np.pi) * dy / r2
    v = strength / (2 * np.pi) * dx / r2
    return u, v
