; ModuleID = 'test.ll'
source_filename = "test.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%struct.anon = type { %struct.Type1*, %struct.Type2* }
%struct.Type1 = type { [8 x i8] }
%struct.Type2 = type { i32, i32* }

@.str = private unnamed_addr constant [30 x i8] c"/////This is a Good function\0A\00", align 1
@.str.1 = private unnamed_addr constant [30 x i8] c"/////This is a Evil function\0A\00", align 1
@gvar = dso_local global %struct.anon zeroinitializer, align 8
@.str.2 = private unnamed_addr constant [5 x i8] c"temp\00", align 1
@handler = dso_local global i32 (i32*)* null, align 8
@.str.3 = private unnamed_addr constant [26 x i8] c"crashing path is taken. \0A\00", align 1
@.str.4 = private unnamed_addr constant [38 x i8] c"..........exploiting path is taken. \0A\00", align 1
@global_a = dso_local global i64 0, align 8
@global_b = dso_local global i64 0, align 8
@handler1 = dso_local global i32 (i32)* null, align 8
@handler2 = dso_local global i32 (i32)* null, align 8

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @goodFunc(i32* %var) #0 {
entry:
  %call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([30 x i8], [30 x i8]* @.str, i64 0, i64 0))
  ret i32 0
}

declare dso_local i32 @printf(i8*, ...) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @badFunc(i32* %var) #0 {
entry:
  %call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([30 x i8], [30 x i8]* @.str.1, i64 0, i64 0))
  ret i32 0
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main(i32 %argc, i8** %argv) #0 {
entry:
  %temp = alloca [16 x i8], align 16
  %call = call noalias align 16 i8* @malloc(i64 8) #4
  %0 = bitcast i8* %call to %struct.Type1*
  store %struct.Type1* %0, %struct.Type1** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 0), align 8
  %call1 = call noalias align 16 i8* @malloc(i64 16) #4
  %1 = bitcast i8* %call1 to %struct.Type2*
  store %struct.Type2* %1, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %arraydecay = getelementptr inbounds [16 x i8], [16 x i8]* %temp, i64 0, i64 0
  call void @klee_make_symbolic(i8* %arraydecay, i64 16, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.2, i64 0, i64 0))
  %arraydecay2 = getelementptr inbounds [16 x i8], [16 x i8]* %temp, i64 0, i64 0
  %2 = load %struct.Type2*, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %status = getelementptr inbounds %struct.Type2, %struct.Type2* %2, i32 0, i32 0
  %3 = bitcast i32* %status to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %3, i8* align 1 %arraydecay2, i64 16, i1 false)
  store i32 (i32*)* @goodFunc, i32 (i32*)** @handler, align 8
  %4 = load %struct.Type2*, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %status3 = getelementptr inbounds %struct.Type2, %struct.Type2* %4, i32 0, i32 0
  %5 = load i32, i32* %status3, align 8
  %tobool = icmp ne i32 %5, 0
  br i1 %tobool, label %if.then, label %if.else

if.then:                                          ; preds = %entry
  %call4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([26 x i8], [26 x i8]* @.str.3, i64 0, i64 0))
  %6 = load %struct.Type2*, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %ptr = getelementptr inbounds %struct.Type2, %struct.Type2* %6, i32 0, i32 1
  %7 = load i32*, i32** %ptr, align 8
  %8 = load i32, i32* %7, align 4
  br label %if.end11

if.else:                                          ; preds = %entry
  %call5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([38 x i8], [38 x i8]* @.str.4, i64 0, i64 0))
  %9 = load %struct.Type2*, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %ptr6 = getelementptr inbounds %struct.Type2, %struct.Type2* %9, i32 0, i32 1
  %10 = load i32*, i32** %ptr6, align 8
  store i32 4660, i32* %10, align 4
  store i64 100, i64* @global_a, align 8
  %tobool7 = icmp ne i32 undef, 0
  br i1 %tobool7, label %if.then8, label %if.else9

if.then8:                                         ; preds = %if.else
  %11 = load i64, i64* @global_a, align 8
  %sub = sub nsw i64 %11, 100
  %12 = inttoptr i64 %sub to i32 (i32*)*
  store i32 (i32*)* %12, i32 (i32*)** @handler, align 8
  br label %if.end

if.else9:                                         ; preds = %if.else
  %13 = load i64, i64* @global_b, align 8
  %sub10 = sub nsw i64 %13, 100
  %14 = inttoptr i64 %sub10 to i32 (i32*)*
  store i32 (i32*)* %14, i32 (i32*)** @handler, align 8
  br label %if.end

if.end:                                           ; preds = %if.else9, %if.then8
  %15 = load i32 (i32*)*, i32 (i32*)** @handler, align 8
  %16 = bitcast i32 (i32*)* %15 to i8*
  %add.ptr = getelementptr i8, i8* %16, i64 1000
  %17 = bitcast i8* %add.ptr to i32 (i32*)*
  store i32 (i32*)* %17, i32 (i32*)** @handler, align 8
  br label %if.end11

if.end11:                                         ; preds = %if.end, %if.then
  %res.0 = phi i32 [ %8, %if.then ], [ undef, %if.end ]
  %18 = load i32 (i32*)*, i32 (i32*)** @handler, align 8
  %19 = load %struct.Type2*, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %ptr12 = getelementptr inbounds %struct.Type2, %struct.Type2* %19, i32 0, i32 1
  %20 = load i32*, i32** %ptr12, align 8
  %call13 = call i32 %18(i32* %20)
  ret i32 %res.0
}

; Function Attrs: nounwind
declare dso_local noalias align 16 i8* @malloc(i64) #2

declare dso_local void @klee_make_symbolic(i8*, i64, i8*) #1

; Function Attrs: argmemonly nofree nounwind willreturn
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* noalias nocapture writeonly, i8* noalias nocapture readonly, i64, i1 immarg) #3

attributes #0 = { noinline nounwind uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nounwind "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { argmemonly nofree nounwind willreturn }
attributes #4 = { nounwind }

!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"uwtable", i32 1}
!2 = !{i32 7, !"frame-pointer", i32 2}
!3 = !{!"clang version 13.0.0 (https://github.com/llvm/llvm-project 35df2f6fbd1ae2e6f9313454e5446212fcbcf90a)"}
