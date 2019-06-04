using UnrealBuildTool;
using System.Collections.Generic;

public class ShindigEditorTarget : TargetRules
{
	public ShindigEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		ExtraModuleNames.Add("Shindig");
	}
}
