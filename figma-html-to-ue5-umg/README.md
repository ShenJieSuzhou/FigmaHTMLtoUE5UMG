# Figma HTML to UE5 UMG

将 Figma Make 或 HTML/CSS 交互式 UI、参考截图和本地 UE5 项目转换为可编辑、可验证的 Unreal Engine 5 UMG Widget Blueprint。

Convert an interactive Figma Make or HTML/CSS UI, reference screenshots, and a local UE5 project into an editable and verifiable Unreal Engine 5 UMG Widget Blueprint.

## What this skill does / 功能

This skill guides Codex through the complete conversion workflow. / 该 Skill 覆盖完整转换流程：

- Analyze HTML, JSX, CSS, screenshots, states, and interactions. / 分析 HTML、JSX、CSS、截图、界面状态和交互逻辑。
- Convert absolute web layouts into native UMG `CanvasPanel` Anchors and Offsets. / 将 Web 绝对定位转换为原生 UMG `CanvasPanel` 的 Anchors 和 Offsets。
- Build native `CanvasPanel`, `Button`, `Border`, `TextBlock`, `Image`, and `Overlay` controls. / 使用原生 UMG 控件搭建层级。
- Map web events to `OnClicked`, `OnHovered`, and `OnUnhovered`. / 将 Web 事件映射到 UMG 事件。
- Create UI-only page transitions, hover states, modal dialogs, scrims, and animations. / 创建页面切换、悬停状态、弹窗、遮罩和动画。
- Export inline SVG icons as tintable Texture2D assets. / 将内嵌 SVG 图标导出为可染色 Texture2D。
- Generate or update Widget Blueprints, optional preview maps, and validation reports. / 创建或更新 WBP、预览地图和验收报告。
- Keep gameplay, level loading, networking, and game rules outside the widget. / 将游戏业务逻辑排除在 Widget 之外。

## Repository layout / 仓库结构

```text
figma-html-to-ue5-umg/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── editor-automation.md
│   └── umg-mapping.md
└── scripts/
    └── extract_inline_svg.py
```

`SKILL.md` contains the main workflow and constraints. The files under `references/` provide detailed UMG mapping and UE5 editor automation guidance. The SVG helper is optional.

`SKILL.md` 是主流程和约束；`references/` 提供 UMG 映射及 UE5 编辑器自动化细节；SVG 工具是可选的。

## Installation / 安装

### Codex desktop or Codex CLI / Codex 桌面版或 CLI

Clone this repository into the Codex skills directory. / 将仓库克隆到 Codex Skill 目录：

```powershell
git clone https://github.com/<your-account>/figma-html-to-ue5-umg.git `
  "$env:USERPROFILE\.codex\skills\figma-html-to-ue5-umg"
```

```bash
git clone https://github.com/<your-account>/figma-html-to-ue5-umg.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/figma-html-to-ue5-umg"
```

If the folder already exists, update it with: / 如果目录已经存在，可以使用：

```bash
git -C "${CODEX_HOME:-$HOME/.codex}/skills/figma-html-to-ue5-umg" pull
```

Windows default path / Windows 默认路径：

```text
C:\Users\<username>\.codex\skills\figma-html-to-ue5-umg
```

macOS and Linux default path / macOS 和 Linux 默认路径：

```text
~/.codex/skills/figma-html-to-ue5-umg
```

Restart or refresh Codex after installation if the skill does not appear in the available skills list.

安装后如果 Skill 没有出现在可用列表中，请重启或刷新 Codex 会话。

### Optional SVG dependency / 可选 SVG 依赖

The included SVG helper requires Python and `resvg-py`. / 内置 SVG 工具需要 Python 和 `resvg-py`：

```bash
python -m pip install resvg-py
```

This dependency is only required for `scripts/extract_inline_svg.py`. The main Skill does not require Python when you only need a written implementation plan.

该依赖只用于 SVG 导出。如果只需要生成 UMG 实施方案，不需要安装 Python 依赖。

## How to use / 使用方法

### Automatic invocation / 自动调用

Once installed, provide the UI source, screenshots, and UE5 project paths in a natural-language request. The Skill is automatically selected when the request clearly asks to convert a web UI into UE5 UMG.

安装后，直接提供 UI 源码、截图和 UE5 项目路径。当请求明确表示要把 Web UI 转换成 UE5 UMG 时，Codex 会自动选择该 Skill。

Example / 示例：

```text
Convert C:\Designs\MainMenu\src and C:\Designs\MainMenu\screenshots
into a UE5 UMG Widget in D:\Projects\MyGame. Create the WBP, export real
image assets, keep gameplay logic as request interfaces, and run validation.
```

### Explicit invocation / 显式调用

Use the skill name to force this workflow. / 可以显式调用该 Skill：

```text
$figma-html-to-ue5-umg

Convert the provided HTML/CSS UI and screenshots into a native UE5 UMG Widget.
```

### Recommended request information / 推荐提供的信息

Provide as much of the following as possible: / 建议尽量提供以下信息：

- Absolute path to the HTML, JSX, TSX, CSS, or Figma Make project. / UI 源码绝对路径。
- Absolute path to reference screenshots. / 参考截图绝对路径。
- Absolute path to the UE5 `.uproject` or project directory. / UE5 项目绝对路径。
- Target UE5 version. / 目标 UE5 版本。
- Whether the user wants a written plan, actual WBP assets, or both. / 需要方案、WBP 资源还是两者都要。
- Allowed UMG controls and whether `EditableTextBox`, `ScrollBox`, `Slider`, `CheckBox`, or `ComboBox` may be used. / 允许使用哪些 UMG 控件。
- Whether to create a preview map and automated UI checks. / 是否创建预览地图和自动化验收。

## Expected output / 预期输出

For an implementation request, the project should contain a scoped UI folder similar to:

对于实际实现请求，项目中应生成类似以下的独立 UI 目录：

```text
Content/UI/MainMenu/
├── WBP_MainMenuRoot.uasset
├── L_UI_MainMenu.umap              # optional / 可选
├── Fonts/
│   └── F_Menu.uasset
└── Textures/
    └── T_UI_*.uasset
```

The implementation report should state the Widget Blueprint path, preview map path if created, widget and animation counts, UI state validation result, and any missing source asset or visual-rendering limitation.

实施报告应说明 Widget Blueprint 路径、预览地图路径、控件和动画数量、UI 状态验收结果，以及缺失源资源或视觉渲染限制。

## UE5 project requirements / UE5 项目要求

For actual WBP generation, the target project should:

实际生成 WBP 时，目标项目应满足：

- Use a supported UE5 version with UMG and editor scripting available.
  使用支持 UMG 和编辑器脚本的 UE5 版本。
- Compile the editor target before running generation commands.
  执行生成命令前先编译 Editor Target。
- Keep generated UI under a scoped path such as `/Game/UI/<Feature>/`.
  将生成资源放在 `/Game/UI/<Feature>/` 等独立目录。
- Avoid replacing existing assets unless the user explicitly requests a rebuild.
  除非用户明确要求重建，否则不要覆盖已有资源。
- Use a legal project font. Orbitron does not contain Chinese glyphs; use a composite font with a Chinese fallback.
  使用合法字体资源。Orbitron 不包含中文字符，需要配置中文 fallback。

## Important limitations / 重要限制

- This Skill creates native UMG. It does not output a browser implementation. / 目标是原生 UMG，不输出浏览器实现。
- CSS `box-shadow`, blur, dashed borders, and complex gradients may require a texture or UI material. / CSS 阴影、模糊、虚线边框和复杂渐变可能需要 Texture 或 UI Material。
- If editable controls are forbidden, a Button/TextBlock approximation cannot provide full Chinese IME composition or native text editing semantics. / 禁止可编辑控件时，Button/TextBlock 不能完整支持中文输入法和原生文本编辑。
- A successful structural or state check does not replace visual PIE testing in the target project. / 结构或状态检查通过不等于完成目标项目 PIE 视觉验收。
- Do not commit proprietary UI source, screenshots, fonts, or game assets to a public repository unless their licenses allow redistribution. / 未获许可证允许时，不要将专有源码、截图、字体或游戏资源提交到公开仓库。

## License / 许可证

Add the license you want to use before publishing this repository. If this Skill remains project-specific, keep the repository private and document the permitted users and projects.

公开发布前，请在仓库中加入你选择的许可证。如果该 Skill 只服务于特定项目，请保持仓库私有，并说明允许使用的用户和项目范围。
