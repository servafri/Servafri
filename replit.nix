{pkgs}: {
  deps = [
    pkgs.run
    pkgs.mongosh
    pkgs.mongodb
    pkgs.dig
    pkgs.postgresql
  ];
}
