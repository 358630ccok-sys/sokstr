# 🎓 Практика Kubernetes + Terraform + Helm — Home-Lab

> Создано: 2026-11-17  
> Цель: подготовка к собеседованию в Банк Уралсиб (Middle DevOps)  
> Среда: Proxmox LXC контейнер (CT200, Debian 12, 192.168.10.240)

---

## 📦 Что установлено

| Инструмент | Версия | Путь | Назначение |
|---|---|---|---|
| **k3s** | v1.37.2 | `/usr/local/bin/k3s` | Легковесный Kubernetes (single-node) |
| **kubectl** | v1.37.2 | `/usr/local/bin/kubectl` (symlink → k3s) | Управление кластером |
| **Helm** | v3.22.1 | `/usr/local/bin/helm` | Пакетный менеджер для K8s |
| **Terraform** | v1.9.8 | `/usr/local/bin/terraform` | IaC (Infrastructure as Code) |
| **Git** | v2.39.5 | `/usr/bin/git` | Контроль версий |

## ✅ Результаты практики (выполнено 2026-11-17)

| # | Упражнение | Статус | Результат |
|---|---|---|---|
| 1 | Базовые команды kubectl | ✅ Выполнено | nginx-demo (2 реплики) развёрнут и работает |
| 2 | Deployment + Service + Ingress | ✅ Выполнено | webapp (3 реплики) + ClusterIP Service + Traefik Ingress |
| 3 | Создание Helm Chart с нуля | ✅ Выполнено | my-webapp chart создан и задеплоен (helm install) |
| 4 | Terraform (локальный провайдер) | ✅ Выполнено | local_file resource создан, apply успешен |
| 5 | Terraform + Kubernetes провайдер | ✅ Выполнено | namespace + deployment (2 реплики) + service через Terraform |
| 6 | Terraform + Yandex Cloud | ✅ Шаблон валидирован | provider установлен, config валиден (нужен YC аккаунт для apply) |

## 🔧 Как подключиться к кластеру

```bash
# SSH на Proxmox
ssh proxmox

# Войти в контейнер
pct exec 200 -- bash

# Настроить окружение (уже сделано, но для надёжности)
export PATH=/usr/local/bin:$PATH
export KUBECONFIG=/root/.kube/config

# Проверить кластер
kubectl get nodes
kubectl get pods -A
```

**Удалённый доступ (с рабочей машины):**
```bash
# Скопировать kubeconfig
scp proxmox:/var/lib/lxc/200/rootfs/root/.kube/config ~/.kube/k8s-lab-config
# Или через pct
ssh proxmox "pct exec 200 -- cat /root/.kube/config" > ~/.kube/k8s-lab-config
# Подключиться
export KUBECONFIG=~/.kube/k8s-lab-config
kubectl get nodes
```

---

## 🧪 Упражнение 1: Базовые команды kubectl

```bash
# Посмотреть ноды
kubectl get nodes -o wide

# Посмотреть все поды
kubectl get pods -A

# Посмотреть поды в namespace
kubectl get pods -n practice

# Описание пода (детали, события)
kubectl describe pod -n practice <pod-name>

# Логи пода
kubectl logs -n practice <pod-name>

# Логи с follow
kubectl logs -f -n practice <pod-name>

# Выполнить команду в поде
kubectl exec -it -n practice <pod-name> -- /bin/sh

# Масштабировать deployment
kubectl scale deployment nginx-demo -n practice --replicas=3
kubectl get pods -n practice

# Удалить ресурсы
kubectl delete -f /tmp/nginx-deploy.yaml
```

---

## 🧪 Упражнение 2: Deployment + Service + Ingress

```yaml
# /tmp/webapp.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  namespace: practice
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: nginx:alpine
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: webapp-svc
  namespace: practice
spec:
  selector:
    app: webapp
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-ingress
  namespace: practice
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
spec:
  rules:
  - host: webapp.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: webapp-svc
            port:
              number: 80
```

**Применить:**
```bash
kubectl apply -f /tmp/webapp.yaml
kubectl get all -n practice
```

---

## 🧪 Упражнение 3: Создание Helm Chart с нуля

```bash
# Создать chart
helm create my-webapp

# Структура:
# my-webapp/
# ├── Chart.yaml          # Метаданные chart
# ├── values.yaml         # Значения по умолчанию
# ├── charts/             # Зависимости
# └── templates/          # Шаблоны K8s манифестов
#     ├── deployment.yaml
#     ├── service.yaml
#     ├── ingress.yaml
#     ├── _helpers.tpl
#     └── NOTES.txt

# Установить chart
helm install my-webapp ./my-webapp -n practice

# Обновить values
helm upgrade my-webapp ./my-webapp -n practice --set replicaCount=3

# Посмотреть историю
helm history my-webapp -n practice

# Откатить
helm rollback my-webapp 1 -n practice

# Удалить
helm uninstall my-webapp -n practice
```

**Пример values.yaml:**
```yaml
replicaCount: 2

image:
  repository: nginx
  tag: alpine
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

resources:
  requests:
    memory: "64Mi"
    cpu: "100m"
  limits:
    memory: "128Mi"
    cpu: "200m"

ingress:
  enabled: true
  className: traefik
  hosts:
    - host: webapp.local
      paths:
        - path: /
          pathType: Prefix
```

---

## 🧪 Упражнение 4: Terraform (локальный провайдер)

```hcl
# /tmp/main.tf
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

resource "local_file" "hello" {
  content  = "Hello from Terraform! Cluster: k3s-lab"
  filename = "/tmp/hello.txt"
}

output "file_path" {
  value = local_file.hello.filename
}
```

```bash
cd /tmp
terraform init
terraform plan
terraform apply -auto-approve
cat /tmp/hello.txt
terraform destroy -auto-approve
```

---

## 🧪 Упражнение 5: Terraform + Kubernetes (k3s провайдер)

```hcl
# /tmp/k8s.tf
terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "kubernetes" {
  config_path = "/root/.kube/config"
}

resource "kubernetes_namespace" "terraform_ns" {
  metadata {
    name = "terraform-practice"
  }
}

resource "kubernetes_deployment" "nginx" {
  metadata {
    name      = "nginx-tf"
    namespace = kubernetes_namespace.terraform_ns.metadata[0].name
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "nginx-tf"
      }
    }
    template {
      metadata {
        labels = {
          app = "nginx-tf"
        }
      }
      spec {
        container {
          name  = "nginx"
          image = "nginx:alpine"
          port {
            container_port = 80
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "nginx_svc" {
  metadata {
    name      = "nginx-tf-svc"
    namespace = kubernetes_namespace.terraform_ns.metadata[0].name
  }
  spec {
    selector = {
      app = "nginx-tf"
    }
    port {
      port        = 80
      target_port = 80
    }
    type = "ClusterIP"
  }
}
```

```bash
cd /tmp
terraform init
terraform plan
terraform apply -auto-approve
kubectl get all -n terraform-practice
terraform destroy -auto-approve
```

---

## 🧪 Упражнение 6: Terraform + Yandex Cloud (шаблон)

```hcl
# /tmp/yc.tf (требует Yandex Cloud аккаунт)
terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.100"
    }
  }
}

provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
  zone      = "ru-central1-a"
}

variable "yc_token" {}
variable "yc_cloud_id" {}
variable "yc_folder_id" {}

resource "yandex_compute_instance" "vm" {
  name        = "devops-practice-vm"
  platform_id = "standard-v2"
  zone        = "ru-central1-a"

  resources {
    cores  = 2
    memory = 4
  }

  boot_disk {
    initialize_params {
      image_id = "fd80bm0rh4rkh30v124m"  # Ubuntu 22.04
      size     = 20
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}

resource "yandex_vpc_network" "network" {
  name = "devops-practice-network"
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "devops-practice-subnet"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["10.0.0.0/24"]
}
```

**Как получить Yandex Cloud credentials:**
1. Создать аккаунт на https://console.cloud.yandex.ru
2. Создать облако и каталог (folder)
3. Получить OAuth-токен: https://oauth.yandex.ru/authorize?response_type=token&client_id=...
4. Узнать cloud_id и folder_id из консоли

---

## 📋 Шпаргалка: частые команды

### kubectl
```bash
# Информация
kubectl get nodes -o wide
kubectl get pods -A
kubectl get svc -A
kubectl get deployments -A
kubectl get ingress -A

# Детали
kubectl describe pod <name> -n <ns>
kubectl describe node <name>

# Логи
kubectl logs <pod> -n <ns>
kubectl logs -f <pod> -n <ns> --tail=100

# Выполнение
kubectl exec -it <pod> -n <ns> -- /bin/sh

# Применение
kubectl apply -f <file.yaml>
kubectl delete -f <file.yaml>

# Масштабирование
kubectl scale deployment <name> -n <ns> --replicas=N

# Порты (port-forward)
kubectl port-forward svc/<name> -n <ns> 8080:80

# Ресурсы
kubectl top nodes
kubectl top pods -A
```

### Helm
```bash
helm repo add <name> <url>
helm repo update
helm search repo <keyword>
helm install <release> <chart> -n <ns>
helm upgrade <release> <chart> -n <ns>
helm rollback <release> <revision> -n <ns>
helm uninstall <release> -n <ns>
helm list -A
helm history <release> -n <ns>
helm get values <release> -n <ns>
```

### Terraform
```bash
terraform init          # Инициализация
terraform plan          # План изменений
terraform apply         # Применить
terraform apply -auto-approve  # Без подтверждения
terraform destroy       # Удалить ресурсы
terraform destroy -auto-approve
terraform fmt           # Форматирование
terraform validate      # Валидация
terraform state list   # Список ресурсов в state
terraform output        # Вывод outputs
```

---

## 🎯 Чеклист для собеседования в Уралсиб

### Kubernetes
- [ ] Объяснить архитектуру (control plane, worker nodes)
- [ ] Назвать основные объекты (Pod, Deployment, Service, ConfigMap, Secret, Ingress, PVC)
- [ ] Показать kubectl команды (get, describe, logs, exec, apply, scale)
- [ ] Объяснить разницу между Deployment и StatefulSet
- [ ] Рассказать про liveness/readiness probes
- [ ] Объяснить что такое namespace и зачем

### Helm
- [ ] Объяснить что такое Helm и зачем
- [ ] Описать структуру chart (Chart.yaml, values.yaml, templates/)
- [ ] Показать helm install/upgrade/rollback
- [ ] Объяснить как работает templating ({{ .Values.xxx }})

### Terraform
- [ ] Объяснить IaC концепцию
- [ ] Описать workflow (init → plan → apply → destroy)
- [ ] Объяснить state и почему он важен
- [ ] Показать provider/resource/output/variable
- [ ] Объяснить разницу между Terraform и Ansible

### Сети
- [ ] OSI модель (7 уровней)
- [ ] TCP vs UDP
- [ ] DNS, DHCP, NAT
- [ ] L4 vs L7 балансировка
- [ ] TLS/SSL, сертификаты

### Мониторинг
- [ ] Prometheus: метрики, exporters, PromQL (базово)
- [ ] Grafana: дашборды, алерты
- [ ] VictoriaMetrics: совместимость с Prometheus
- [ ] ELK/Vector: централизованное логирование

---

## 🔗 Полезные ссылки

- **Kubernetes docs:** https://kubernetes.io/docs/
- **Helm docs:** https://helm.sh/docs/
- **Terraform docs:** https://developer.hashicorp.com/terraform/docs
- **Yandex Cloud Terraform:** https://terraform-provider.yandexcloud.net/
- **k3s docs:** https://docs.k3s.io/
- **Proxmox LXC:** https://pve.proxmox.com/wiki/Linux_Container

---

## 📝 Заметки

- Контейнер CT200: 192.168.10.240, 4GB RAM, 2 cores, Debian 12
- k3s работает в режиме single-node (control plane + worker на одном узле)
- Для production K8s нужен multi-node кластер (но для обучения достаточно)
- Yandex Cloud: создать бесплатный аккаунт на https://console.cloud.yandex.ru
- Для практики с Terraform + Yandex Cloud нужен OAuth-токен и cloud_id/folder_id
- VMware: запустить на Proxmox невозможно, но концепции виртуализации (VM, storage, networking) переносимы из Proxmox опыта
