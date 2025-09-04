try:
    import tensorflow as tf
    print("TensorFlow is still installed!")
except ImportError:
    print("No TensorFlow detected (good).")