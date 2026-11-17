# 🏗️ Статус DevOps/MLOps лаборатории на Proxmox

> Дата развёртывания: **2026-11-17**  
> Платформа: **Proxmox VE** (хост: `192.168.10.100`)  
> Цель: hands-on практика **Kubernetes, Helm, Terraform, Ansible** для позиции Middle DevOps (в т.ч. Уралсиб)

---

## ✅ Что развёрнуто (сводка)

| Компонент | Где | Версия / состояние | Статус |
|---|---|---|---|
| **Kubernetes (k3s)** | LXC CT200 `k8s-lab` (`192.168.10.240`) | `v1.37.2+k3s1`, node **Ready**, control-plane | ✅ Развёрнуто и работает |
| **kubectl** | CT200 `/usr/local/bin/kubectl` | `v1.37.2+k3s1` | ✅ Установлен |
| **Helm** | CT200 `/usr/local/bin/helm` | `v3.22.1` | ✅ Установлен, chart задеплоен |
| **Terraform** | CT200 `/usr/local/bin/terraform` | `v1.9.8` | ✅ Установлен, apply выполнен |
| **Ansible** | CT200 `/usr/bin/ansible` | `ansible-core 2.14.18` (Debian pkg) | ✅ Установлен, playbooks выполнены |

---

## 🖥️ Среда (контейнер для практики)

| Параметр | Значение |
|---|---|
| **Proxmox хост** | `192.168.10.100` |
| **CT ID** | `200` |
| **Hostname** | `k8s-lab` |
| **IP** | `192.168.10.240` (DHCP, vmbr0) |
| **OS** | Debian 12 (bookworm), unprivileged LXC, nesting=1 |
| **Ресурсы** | 4 GB RAM, 2 vCPU, 20 GB disk (`local:20`) |
| **Шаблон** | `debian-12-standard_12.12-1_amd64.tar.zst` |

---

## ☸️ Kubernetes (k3s) — что запущено

**Кластер:** single-node k3s (`k8s-lab`, Ready)

### Namespaces и workloads (практика)
| Namespace | Ресурсы | Назначение |
|---|---|---|
| `kube-system` | CoreDNS, Traefik, metrics-server, local-path-provisioner, svclb | Системные компоненты k3s |
| `practice` | `nginx-demo` (2), `webapp` (3) + Service + Ingress, `my-webapp` (Helm) | Ручные манифесты + Helm |
| `terraform-practice` | `nginx-tf` (2) + Service | Создано через Terraform Kubernetes provider |
| `ansible-practice` | `ansible-nginx` (2) + Service | Создано через Ansible playbook |

### Выполненные упражнения K8s/Helm
- ✅ Базовые `kubectl` (get/describe/logs/exec/scale)
- ✅ Deployment + Service (ClusterIP) + Ingress (Traefik, `webapp.local`)
- ✅ Helm chart создан (`helm create my-webapp`) и задеплоен (`helm install`)

---

## 🌍 Terraform — что выполнено

| Упражнение | Провайдер | Результат |
|---|---|---|
| Local provider | `hashicorp/local` | ✅ `local_file` создан (`/tmp/hello-terraform.txt`), `apply` успешен |
| Kubernetes provider | `hashicorp/kubernetes` | ✅ Namespace + Deployment(2) + Service созданы в `terraform-practice` |
| Yandex Cloud | `yandex-cloud/yandex` | ✅ Провайдер установлен, конфиг валиден (`terraform validate`) — **для `apply` нужен YC аккаунт/токены** |

> Примечание: провайдеры установлены локально (offline plugin-dir) из-за сетевых ограничений/прокси в окружении.

---

## 🤖 Ansible — что развёрнуто и выполнено

**Лаборатория:** `/root/ansible-lab/` (CT200)

**Структура:**
- `ansible.cfg` — конфигурация (local inventory, yaml output)
- `inventory/hosts.ini` — группы `local`, `k3s`
- `playbooks/01-ping.yml` — проверка подключения ✅
- `playbooks/02-system-info.yml` — сбор фактов/информации о системе ✅
- `playbooks/03-install-packages.yml` — идемпотентная установка пакетов (curl/wget/git/htop/jq) ⚠️ зависит от доступности apt-репозиториев/прокси
- `playbooks/04-deploy-k8s-app.yml` — деплой приложения в k3s через Ansible ✅ (idempotent)
- `playbooks/05-verify-k8s.yml` — проверка нод/подов кластера ✅
- `roles/nginx/tasks/main.yml` + `roles/nginx/templates/*.j2` — рабочая роль (деплой nginx в k3s)
- `group_vars/all.yml`, `files/` — переменные и файлы для роли

**Результат практики:** Ansible успешно управляет локальным хостом и деплоит манифесты в k3s (`ansible-practice` namespace).

---

## 🔌 Как подключиться и проверить

### 1) Войти в лабораторию
```bash
ssh proxmox
pct exec 200 -- bash
export PATH=/usr/local/bin:$PATH
export KUBECONFIG=/root/.kube/config
export LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
```

### 2) Проверить Kubernetes
```bash
kubectl get nodes -o wide
kubectl get pods -A
kubectl get svc -A
kubectl get ingress -A
```

### 3) Проверить Helm
```bash
helm version
helm list -A
```

### 4) Проверить Terraform
```bash
terraform version
cd /tmp/tf-local && terraform state list
cd /tmp/tf-k8s && terraform state list
```

### 5) Проверить Ansible
```bash
cd /root/ansible-lab
ansible --version
ansible-playbook playbooks/01-ping.yml
ansible-playbook playbooks/05-verify-k8s.yml
```

---

## 📈 Прогресс подготовки (Уралсиб / Middle DevOps)

| Область | Статус | Что подтверждено |
|---|---|---|
| Linux / on-prem | ✅ | Proxmox, LXC, Debian, эксплуатация |
| Docker / контейнеры | ✅ | Сервисы в контейнерах, k3s workloads |
| Kubernetes | ✅ Hands-on | k3s, kubectl, Deployment/Service/Ingress, namespaces |
| Helm | ✅ Hands-on | Создание и деплой chart |
| Terraform | ✅ Hands-on | Local + Kubernetes providers, YC config подготовлен |
| Ansible | ✅ Hands-on | Inventory, playbooks, деплой в k3s, факты/проверки |
| CI/CD / мониторинг (home-lab) | ✅ | GitLab/Runner, Prometheus/Grafana, n8n (основная платформа) |

**Следующие шаги (опционально):**
- Создать Yandex Cloud аккаунт и выполнить `terraform apply` для YC (нужны `token/cloud_id/folder_id`)
- Добавить Ansible роли (nginx/system hardening) и multi-host inventory
- Развернуть multi-node K8s (если понадобятся ресурсы/VM)
- Практика сетей/логирования (ELK/Vector, VictoriaMetrics) по плану интервью
