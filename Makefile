# 可用的 IDE 列表
IDES := github-copilot cursor windsurf

# 可用的任务列表 (不包含 .md 后缀)
TASKS := 1-logical-reasoning-and-algorithm \
         2-context-understanding-and-system-architecture \
         3-error-handling-and-robustness \
         4-performance-optimization-and-resource-management \
         5-creative-problem-solving-and-complex-requirements

# 默认值
IDE ?= $(shell gum choose $(IDES))
TASK ?= $(shell gum choose $(TASKS))

.PHONY: clean evaluate

# 清理命令 - 删除指定 IDE 目录下的所有文件
clean:
	@echo "请选择要清理的 IDE..."
	@IDE=$$(gum choose $(IDES)) && \
	if [ -d "ides/$$IDE" ]; then \
		rm -rf "ides/$$IDE"/* && \
		echo "已清理 ides/$$IDE 目录" || \
		echo "清理目录时发生错误"; \
	else \
		echo "目录 ides/$$IDE 不存在"; \
	fi

# 评估命令 - 运行指定 IDE 和任务的评估
evaluate:
	@echo "请选择要评估的 IDE..."
	@IDE=$$(gum choose $(IDES)) && \
	echo "请选择要评估的任务..." && \
	TASK=$$(gum choose $(TASKS)) && \
	echo "请选择要评估的代码文件:" && \
	CODE_FILE=$$(find "ides/$$IDE" -type f -not -path '*/\.*' | sed "s|^./||" | gum choose) && \
	python evaluate.py "tasks/$$TASK.md" "$$CODE_FILE"
