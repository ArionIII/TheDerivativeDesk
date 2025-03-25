LINEAR_ALGEBRA_AND_ADVANCED_CALCULATION_TOOL_CONFIG = {
    "singular-value-decomposition": {
        "title": "Singular Value Decomposition (SVD)",
        "description": "Perform SVD for dimensionality reduction and feature extraction.",
        "url": "/tools/linear-algebra-tools/singular-value-decomposition",
        "inputs": [
            {
                "label": "Matrix",
                "id": "matrix",
                "type": "array",
                "placeholder": "[[1, 2], [3, 4]]",
                "optional": False,
            },
        ],
        "outputs": ["U Matrix", "Sigma (Singular Values)", "V Transposed"],
    },
    "principal-component-analysis": {
        "title": "Principal Component Analysis (PCA)",
        "description": "Conduct PCA for feature extraction and data compression.",
        "url": "/tools/advanced-calculations/principal-component-analysis",
        "inputs": [
            {
                "label": "Data Matrix",
                "id": "data_matrix",
                "type": "array",
                "placeholder": "[[1, 2], [3, 4], [5, 6]]",
                "optional": False,
            },
        ],
        "outputs": ["Principal Components", "Explained Variance"],
    },
    "eigenvalues-eigenvectors": {
        "title": "Eigenvalues and Eigenvectors",
        "description": "Compute eigenvalues and eigenvectors for matrix transformations.",
        "url": "/tools/advanced-calculations/eigenvalues-eigenvectors",
        "inputs": [
            {
                "label": "Matrix",
                "id": "matrix",
                "type": "array",
                "placeholder": "[[1, 2], [3, 4]]",
                "optional": False,
            },
        ],
        "outputs": ["Eigenvalues", "Eigenvectors"],
    },
    "matrix-multiplication": {
        "title": "Matrix Multiplication",
        "description": "Compute the product of matrices.",
        "url": "/tools/linear-algebra-tools/matrix-multiplication",
        "inputs": [
            {
                "label": "Matrix A",
                "id": "matrix_a",
                "type": "array",
                "placeholder": "[[1, 2], [3, 4]]",
                "optional": False,
            },
            {
                "label": "Matrix B",
                "id": "matrix_b",
                "type": "array",
                "placeholder": "[[5, 6], [7, 8]]",
                "optional": False,
            },
        ],
        "outputs": ["Matrix Product"],
    },
    "inverse-matrices": {
        "title": "Inverse Matrices",
        "description": "Calculate the inverse of a matrix.",
        "url": "/tools/linear-algebra-tools/inverse-matrices",
        "inputs": [
            {
                "label": "Matrix",
                "id": "matrix",
                "type": "array",
                "placeholder": "[[1, 2], [3, 4]]",
                "optional": False,
            },
        ],
        "outputs": ["Inverse Matrix"],
    },
}
