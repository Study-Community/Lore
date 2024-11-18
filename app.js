const knowledge = {
    "math": {
        "algebra": {
            "linear_algebra": {
                "vector_spaces": "advanced",
                "matrices": "intermediate"
            },
            "abstract_algebra": {
                "groups": "intermediate",
                "rings": "beginner"
            }
        },
        "calculus": {
            "differential_calculus": {
                "limits": "advanced",
                "derivatives": "advanced"
            },
            "integral_calculus": {
                "definite_integrals": "intermediate",
                "indefinite_integrals": "intermediate"
            }
        },
        "geometry": {
            "euclidean_geometry": {
                "points": "advanced",
                "lines": "advanced"
            },
            "non_euclidean_geometry": {
                "hyperbolic_geometry": "beginner",
                "elliptic_geometry": "beginner"
            }
        }
    }
};

function displayKnowledge(knowledge, container) {
    for (const key in knowledge) {
        if (typeof knowledge[key] === 'object') {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'category';
            categoryDiv.textContent = key;
            container.appendChild(categoryDiv);
            displayKnowledge(knowledge[key], categoryDiv);
        } else {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'item';
            itemDiv.textContent = `${key}: `;
            const button = document.createElement('button');
            button.textContent = knowledge[key];
            button.onclick = () => alert(`Knowledge level: ${knowledge[key]}`);
            itemDiv.appendChild(button);
            container.appendChild(itemDiv);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('knowledge-container');
    displayKnowledge(knowledge, container);
});