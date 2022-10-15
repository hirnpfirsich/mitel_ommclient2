{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs, ... }: {
    packages.x86_64-linux = let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
    in {
      mitel-ommclient2 = pkgs.python3Packages.buildPythonPackage rec {
        pname = "mitel-ommclient2";
        version = "0.0.1";

        src = ./.;

        outputs = [
          "out"
          "doc"
        ];

        nativeBuildInputs = [
          pkgs.python3Packages.sphinxHook
        ];

        format = "pyproject";

        buildInputs = [ pkgs.python3Packages.hatchling ];
        propagatedBuildInputs = [ pkgs.python3Packages.rsa ];

        pythonImportsCheck = [ "mitel_ommclient2" ];
      };
    };

    hydraJobs = {
      inherit (self)
        packages;
    };
  };
}
