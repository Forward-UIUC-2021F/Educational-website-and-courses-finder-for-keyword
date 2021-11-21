from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.metrics import precision_score, recall_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import itertools

random_seed = 17

# Load dataset
df = pd.read_excel(r'E:\Learning\undergraduate\2021 Fall\CS397\data_labeling.xlsx', sheet_name='dataset')
x = df.iloc[:, [0, 24]].values
labels = df.iloc[:, 25].values

train, test, train_labels, test_labels = train_test_split(x, labels, stratify = labels, test_size=0.3, random_state = random_seed)

model = RandomForestClassifier(n_estimators = 100,
                               random_state = random_seed,
                               max_features = 'sqrt')

# Fit on training data
model.fit(train, train_labels)

# Training predictions (to demonstrate overfitting)
train_rf_predictions = model.predict(train)
train_rf_probs = model.predict_proba(train)[:, 1]

# Testing predictions (to determine performance)
rf_predictions = model.predict(test)
rf_probs = model.predict_proba(test)[:, 1]

print('Accuracy:',accuracy_score(test_labels, rf_predictions))


# Plot formatting
plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 18


def evaluate_model(predictions, probs, train_predictions, train_probs):
    """Compare machine learning model to baseline performance.
    Computes statistics and shows ROC curve."""

    baseline = {}

    """ Note that the 'baseline' here is set by making all predictions for test_data to be 'useful' """
    baseline['recall'] = recall_score(test_labels,
                                      [1 for _ in range(len(test_labels))],average = 'micro')
    baseline['precision'] = precision_score(test_labels,
                                            [1 for _ in range(len(test_labels))],average = 'micro')
    baseline['roc'] = 0.5

    results = {}

    results['recall'] = recall_score(test_labels, predictions,average = 'micro')
    results['precision'] = precision_score(test_labels, predictions,average = 'micro')
    # results['roc'] = roc_auc_score(test_labels, probs,average = 'micro')

    train_results = {}
    train_results['recall'] = recall_score(train_labels, train_predictions,average = 'micro')
    train_results['precision'] = precision_score(train_labels, train_predictions,average = 'micro')
    # train_results['roc'] = roc_auc_score(train_labels, train_probs)

    for metric in ['recall', 'precision']:
        print(
            f'{metric.capitalize()} Baseline: {round(baseline[metric], 2)} Test: {round(results[metric], 2)} Train: {round(train_results[metric], 2)}')

    # Calculate false positive rates and true positive rates
    # base_fpr, base_tpr, _ = roc_curve(test_labels, [1 for _ in range(len(test_labels))])
    # model_fpr, model_tpr, _ = roc_curve(test_labels, probs)

    # plt.figure(figsize=(8, 6))
    # plt.rcParams['font.size'] = 16
    #
    # # Plot both curves
    # plt.plot(base_fpr, base_tpr, 'b', label='baseline')
    # plt.plot(model_fpr, model_tpr, 'r', label='model')
    # plt.legend()
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.title('ROC Curves of Random Forest')
    # plt.show()


evaluate_model(rf_predictions, rf_probs, train_rf_predictions, train_rf_probs)
# plt.savefig('roc_auc_curve.png')


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Oranges):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    Source: http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    # Plot the confusion matrix
    plt.figure(figsize=(10, 10))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, size=24)
    plt.colorbar(aspect=4)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, size=14)
    plt.yticks(tick_marks, classes, size=14)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.

    # Labeling the plot
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt), fontsize=20,
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.grid(None)
    plt.tight_layout()
    plt.ylabel('True label', size=18)
    plt.xlabel('Predicted label', size=18)
    plt.title('Confusion Matrix of Random Forest')
    plt.show()


# Confusion matrix
cm = confusion_matrix(test_labels, rf_predictions)
plot_confusion_matrix(cm, classes=['Not useful', 'Useful','very useful'])

# plt.savefig('cm.png')

