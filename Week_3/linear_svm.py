from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def svm_loss_naive(W, X, y, reg):
    """
    Structured SVM loss function, naive implementation (with loops).

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    dW = np.zeros(W.shape)  # initialize the gradient as zero

    # compute the loss and the gradient
    num_classes = W.shape[1]  # C
    num_train = X.shape[0]  # N
    loss = 0.0
    for i in range(num_train):
        scores = X[i].dot(W)
        correct_class_score = scores[y[i]]
        for j in range(num_classes):
            if j == y[i]:
                continue
            margin = scores[j] - correct_class_score + 1  # note delta = 1
            if margin > 0:  # SVM = max(0, )
                loss += margin

                # dL = dW * d(sj-syi+1)
                # s = XW -> ds * dW = dX
                # dL = dXj - dXyi
                dW[:, j] += X[i, :]  # i-th data's D == j class's D
                dW[:, y[i]] -= X[i, :]  # i-th data's D == y[i] class's D

    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by num_train.
    loss /= num_train
    dW /= num_train

    # Add regularization to the loss.
    # lambda * R(W^2)
    loss += reg * np.sum(W * W)

    # gradient of the loss function
    dW += 2*reg*W

    #############################################################################
    # TODO:                                                                     #
    # Compute the gradient of the loss function and store it dW.                #
    # Rather than first computing the loss and then computing the derivative,   #
    # it may be simpler to compute the derivative at the same time that the     #
    # loss is being computed. As a result you may need to modify some of the    #
    # code above to compute the gradient.                                       #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def svm_loss_vectorized(W, X, y, reg):
    """
    Structured SVM loss function, vectorized implementation.

    Inputs and outputs are the same as svm_loss_naive.
    """
    loss = 0.0
    dW = np.zeros(W.shape)  # initialize the gradient as zero

    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the structured SVM loss, storing the    #
    # result in loss.                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_classes = W.shape[1]  # C
    num_train = X.shape[0]  # N

    scores = np.matmul(X, W)
    correct_class_score = scores[range(num_train), y].reshape(num_train, 1)

    margin = np.maximum(0, scores - correct_class_score + 1)
    margin[range(num_train), y] = 0  # answer col -> margin == 0
    loss = margin.sum() / num_train  # loss = sum of the entire loss

    # Add regularization to the loss.
    loss += reg * np.sum(W * W)

    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the gradient for the structured SVM     #
    # loss, storing the result in dW.                                           #
    #                                                                           #
    # Hint: Instead of computing the gradient from scratch, it may be easier    #
    # to reuse some of the intermediate values that you used to compute the     #
    # loss.                                                                     #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # dL = dW * d(sj-syi+1)
    # s = XW -> ds * dW = dX
    margin_exclusive = np.zeros(margin.shape)
    margin_exclusive[margin > 0] = 1  # false case
    # dW[:, y[i]] -= X[i, :]
    # answer column - loop number
    margin_exclusive[range(num_train), y] -= np.sum(margin_exclusive, axis=1)

    # dL = dXj - dXyi
    dW = np.matmul(X.T, margin_exclusive) / num_train

    dW += 2*reg*W

    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
