# Trained Models Directory

## Place Your CNN Model Here

This directory should contain your trained CNN model for face emotion recognition.

### Required File

- `cnn_face_emotion.pth` - Your trained PyTorch model weights

### Model Requirements

1. **Architecture Match**: The model architecture in `app/models/ml_models/cnn_architecture.py` must match your trained model

2. **Input Format**:
   - Grayscale images
   - Size: 48x48 pixels
   - Normalized to [0, 1]
   - Shape: (batch_size, 1, 48, 48)

3. **Output Format**:
   - 7 classes (emotions)
   - Order: angry, disgust, fear, happy, sad, surprise, neutral

### How to Add Your Model

```bash
# Copy your trained model to this directory
cp /path/to/your/model.pth ./cnn_face_emotion.pth

# Verify the model works
python scripts/test_model_inference.py
```

### Model Architecture Options

The codebase provides two architectures:

1. **EmotionCNN** (default) - Deeper CNN with batch normalization
2. **SimpleCNN** - Lighter CNN for faster inference

Choose the one that matches your training, or modify `cnn_architecture.py` to match your exact architecture.

### Training Your Own Model

If you need to train a model:

1. Use FER2013 or similar emotion recognition dataset
2. Ensure 48x48 grayscale input
3. Train with 7 emotion classes
4. Save model weights: `torch.save(model.state_dict(), 'cnn_face_emotion.pth')`

### Model Metadata

Update `model_config.json` with your model's details:
- Architecture name
- Training accuracy
- Dataset used
- Hyperparameters

This helps with versioning and troubleshooting.
