#!/usr/bin/env python
import logging

from benderthon import tf_freeze
import numpy as np
import tensorflow as tf


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    x = tf.placeholder(tf.float32, shape=(1, 2, 3))
    y = tf.placeholder(tf.float32, shape=(4, 2, 3))
    z = tf.placeholder(tf.float32, shape=(5, 6, 3))
    a = tf.placeholder(tf.float32, shape=(5, 8, 7))

    c1 = tf.concat([x, y], axis=0)
    c2 = tf.concat([c1, z], axis=1)
    c3 = tf.concat([c2, a], axis=2, name='output')

    tf.Variable(0, name='dummy')

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        # noinspection PyUnresolvedReferences,PyProtectedMember
        x_len = np.prod(x.shape)._value
        # noinspection PyUnresolvedReferences,PyProtectedMember
        y_len = np.prod(y.shape)._value
        # noinspection PyUnresolvedReferences,PyProtectedMember
        z_len = np.prod(z.shape)._value
        # noinspection PyUnresolvedReferences,PyProtectedMember
        a_len = np.prod(a.shape)._value

        saver = tf.train.Saver(allow_empty=True)
        checkpoint_path = 'test_concat.ckpt'

        saver.save(sess, checkpoint_path)

        print(sess.run(c3, {x: np.arange(x_len).reshape(x.shape),
                            y: (np.arange(y_len) + x_len).reshape(y.shape),
                            z: (np.arange(z_len) + x_len + y_len).reshape(z.shape),
                            a: (np.arange(a_len) + x_len + y_len + z_len).reshape(a.shape)}))

        tf_freeze.freeze_from_checkpoint(checkpoint_path, 'test_concat.pb', ['output'])
        # tf_freeze.save_graph_only(sess, 'test_concat.pb', ['output'])
