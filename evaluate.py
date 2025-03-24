import os

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import os
from http import HTTPStatus
from dashscope import Application

load_dotenv()

console = Console()

# 评估提示模板
PROMT_EVALUATE = """
你是一位经验丰富的编程专家，被要求评估AI生成的代码。你的目标是对代码的质量、功能性和性能进行全面评估, 总字数 200 字以内。以下是任务详情：

任务描述：
<task_description>
{TASK_DESCRIPTION}
</task_description>

AI生成的代码：
<ai_generated_code>
{AI_GENERATED_CODE}
</ai_generated_code>

在开始评估之前，请仔细考虑你将从以下维度评估代码, 每项评分标准（1.0-5.0 分, 最小差别是 0.1）：
1. 功能正确性
2. 算法准确性
3. 代码质量
4. 性能
5. 健壮性
6. 创造性和创新性（对于开放性任务）

对于每个维度，你将提供详细分析。在<dimension_analysis>标签内展示你对每个标准的思考过程。在分析所有维度后，提供你的评分和发现摘要。

评估过程：

首先，在<code_overview>标签中列出与每个维度相关的代码关键方面。这将有助于确保全面分析。请务必详细且具体地描述每个方面，并引用代码中的具体部分。

然后，按以下步骤进行每个维度的分析：

1. 功能正确性：
   <dimension_analysis>
   - 验证代码是否正确实现了所需功能。提供具体的代码示例来支持你的观点。
   - 创建至少3个测试用例（正常情况、边界情况和特殊情况）并检查代码的输出。详细写出每个测试用例，包括输入和预期输出。
   - 执行代码并记录实际输出结果。比较预期输出和实际输出，解释任何差异。
   - 如果存在问题，请明确指出并提供具体的修复建议，包括代码示例。
   </dimension_analysis>

2. 算法准确性：
   <dimension_analysis>
   - 如果需要特定算法，检查其是否正确实现。引用代码中的具体部分来支持你的分析。
   - 详细列出算法的主要步骤，并与代码实现进行逐步比较。
   - 深入分析代码的逻辑流程，并与算法的理论描述进行详细比较。提供具体的代码片段作为例证。
   - 执行代码并验证算法的输出是否符合预期。提供具体的输入输出示例。
   - 如果存在错误，详细解释它们并提供正确的实现方法，包括代码示例。
   </dimension_analysis>

3. 代码质量：
   <dimension_analysis>
   - 评估代码的结构、命名约定和注释。提供具体的良好和不良实践示例。
   - 详细统计并列出良好和不良做法的具体实例，包括代码片段。
   - 评估模块化程度和易于理解/维护的程度。提供具体的例子来说明你的观点。
   - 如果质量不足，指出具体问题并提供详细的改进建议，包括代码示例。
   </dimension_analysis>

4. 性能：
   <dimension_analysis>
   - 详细分析时间和空间复杂度，提供具体的计算过程和结果。
   - 评估大规模数据场景下的性能。提供具体的性能预测和潜在问题。
   - 如果存在性能瓶颈，提供具体的优化建议，包括代码示例和预期的性能提升。
   - 如果可能，执行基准测试并详细报告结果，包括测试环境、输入数据和性能指标。
   </dimension_analysis>

5. 健壮性：
   <dimension_analysis>
   - 详细列出你要测试的边界情况和错误条件，解释为什么选择这些情况。
   - 使用这些边界情况（空输入、非常大的输入）和错误条件测试代码。提供具体的测试用例和结果。
   - 详细评估错误处理和用户反馈的适当性。提供具体的代码示例和改进建议。
   - 执行代码并验证其在各种输入情况下的行为。详细记录每种情况的结果。
   - 如果健壮性不足，明确指出问题并提供详细的修复方法，包括代码示例。
   </dimension_analysis>

6. 创造性和创新性（对于开放性任务）：
   <dimension_analysis>
   - 详细列出你在实现中发现的任何独特或创新元素。提供具体的代码示例来说明这些元素。
   - 深入评估代码是否展示了创新解决方案或独特的设计方法。解释为什么这些方法是创新的。
   - 如果缺乏创新，提出详细的潜在改进或替代方法建议，包括代码示例和预期效果。
   </dimension_analysis>

完成分析后，请按以下格式提供评估摘要：

<summary>
评分: [先列出每项得分, 然后根据各项目相加计算总分]
整体质量：[详细说明代码的整体质量，包括各个维度的综合评估]

优点：
- [列出主要优点，每个优点都要有具体的代码示例或分析支持]

需要改进的地方：
- [列出主要需要改进的地方，每个问题都要有具体的改进建议和代码示例]

结论：[详细说明代码是否满足任务要求，总结各个维度的表现，并提供最终建议和改进方向]
</summary>

请记住：
- 在整个评估过程中保持客观性，提供具体的证据和示例来支持你的观点。
- 对于复杂任务，优先考虑功能正确性和算法准确性，但不要忽视其他维度。
- 特别注意任务描述或评估标准中特别强调的任何维度，并在分析中给予额外关注。
- 在每个分析步骤中，提供尽可能详细和具体的信息，包括代码示例、测试用例和性能数据。
- 仔细检查评分计算是否正确, 尤其是相加操作

现在，请开始评估AI生成的代码，确保你的分析全面、深入且有具体依据。
"""


def evaluate_code(task_description, ai_generated_code):
    # 使用进度指示器显示等待状态
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="正在等待 LLM 响应...", total=None)
        response = Application.call(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            app_id='aabac58fe99e4cbb81077e9a1ce2299e',
            prompt=PROMT_EVALUATE.format(
                        TASK_DESCRIPTION=task_description,
                        AI_GENERATED_CODE=ai_generated_code,
                    )
        )
    return response.output.text


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        console.print(
            Panel.fit(
                "[red]错误：参数数量不正确[/red]\n用法：python evaluate.py <任务文件.md> <代码文件.py>",
                title="错误",
                border_style="red",
            )
        )
        sys.exit(1)

    task_file = sys.argv[1]
    code_file = sys.argv[2]

    console.print(
        Panel.fit(
            f"[bold blue]任务文件：[/bold blue] {task_file}\n[bold blue]代码文件：[/bold blue] {code_file}",
            title="开始评估",
            border_style="blue",
        )
    )

    with open(task_file, "r") as f:
        task_description = f.read()

    with open(code_file, "r") as f:
        ai_generated_code = f.read()

    result = evaluate_code(
        task_description,
        ai_generated_code,
    )

    # 从文件路径中提取 IDE 名称和任务名称
    ide_name = code_file.split("/")[1]  # 例如：ides/cursor/1.ts -> cursor
    task_name = task_file.split("/")[-1].split(".")[
        0
    ]  # 例如：tasks/1-logical-reasoning-and-algorithm.md -> 1-logical-reasoning-and-algorithm
    result_file_name = f"results/{ide_name}/e_{task_name}.md"

    # 创建结果目录（如果不存在）并保存结果
    os.makedirs(os.path.dirname(result_file_name), exist_ok=True)
    with open(result_file_name, "w") as f:
        f.write(result)

    console.print(
        Panel.fit(
            f"[green]评估完成！[/green]\n结果已保存至： {result_file_name}",
            title="成功",
            border_style="green",
        )
    )
