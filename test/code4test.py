"""
generate permutation
"""


def generate_permutation(n):
    permutation_index = np.random.permutation(n)
    return permutation_index


def plot_permutation(perm):
    plt.figure(figsize=(10,8))
    plt.subplot(2,2,1)
    plt.title('permutation')