# Yolov5_Honor-of-Kings

## 如何使用？

### 安装依赖项

```bash
git clone https://github.com/chancey922/Yolov5_Honor-of-Kings.git
cd Yolov5_Honor-of-Kings

# 安装必要的package
pip install -r requirements.txt
# 安装wandb进行项目跟踪可视化，不使用的可以安装
pip install wandb
```

## 配置`yaml`

### 训练模型

```python
python train.py \
  --img 640 \
  --batch 16  \
  --epochs 300  \
  --data /content/Yolov5_Honor-of-Kings/src/train.yaml \
  --weights yolov5l.pt  \
  --project Yolo-wandb-wzry \
  --upload_dataset \
  --save_period 50 \
  --cache 
```

