using UnrealBuildTool;
using System.Collections.Generic;

public class ShindigTarget : TargetRules
{
	public ShindigTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		ExtraModuleNames.Add("Shindig");
	}
}
