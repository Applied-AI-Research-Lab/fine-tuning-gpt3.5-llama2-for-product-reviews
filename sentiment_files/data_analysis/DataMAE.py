import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error


def plot(model, model_title):
    # Read data from CSV
    data = pd.read_csv('../datasets/research-results.csv')

    # Count mean absolute error
    mae = mean_absolute_error(data['review_rating'], data[model])

    # Εκτυπώστε το MAE
    print(f"{model_title}: {mae}")

    x = data['review_rating']
    y = data[model]
    error = data['review_rating'] - data[model]

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label='"' + model_title + '" Predictions vs. "review_rating"')
    plt.plot(x, x, color='red', linestyle='--', label='Perfect Fit Line')
    plt.legend()
    plt.title(f'MAE: {mae:.2f}')
    plt.xlabel('review_rating')
    plt.ylabel(model_title)
    plt.show()

plot('gpt', 'base:gpt-3.5-turbo-1106')
plot('llama', 'base:llama-2-70b-chat')
plot('ft_gpt_100', 'ft:gpt-3.5-turbo-1106 (100%)')
plot('ft_llama_100', 'ft:llama-2-70b-chat (100%)')
plot('ft_bert_adam_100', 'ft:bert-adam (100%)')
plot('ft_roberta_adam_100', 'ft:roberta-adam (100%)')